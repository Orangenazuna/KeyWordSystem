# llm_local.py
import requests

# Ollama HTTP endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# 用 curl 查到的实际模型名
MODEL_NAME = "qwen3:8b"

def call_local_llm(prompt: str) -> str:
    """
    把 prompt 发给本地 Ollama (Qwen3:8b) 并拿到回答。
    如果 Ollama 没跑 / 模型名不对，就返回一个友好的报错字符串，
    避免直接把 Streamlit 弹红。
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    except requests.exceptions.ConnectionError:
        return "[LLM错误] 无法连接到 Ollama (http://localhost:11434)。请确认 Ollama 正在运行。"
    except Exception as e:
        return f"[LLM异常] 发送到 Ollama 时出错: {e}"

    if resp.status_code != 200:
        # 比如模型名找不到时 Ollama 会返回 404
        try:
            err_detail = resp.json()
        except Exception:
            err_detail = resp.text
        return f"[LLM错误] Ollama返回了状态码 {resp.status_code}，可能模型名不匹配。详情: {err_detail}"

    data = resp.json()
    answer = data.get("response", "").strip()
    if not answer:
        return "[LLM错误] Ollama没有返回内容。"
    return answer

if __name__ == "__main__":
    test_prompt = "用中文回答：你现在是本地推理的Qwen3:8b吗？请简短介绍你的能力。"
    print(call_local_llm(test_prompt))
