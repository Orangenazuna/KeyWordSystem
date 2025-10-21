# rag_engine.py

# 1. 导入向量库和embedding
from langchain_community.vectorstores import Chroma

# Embedding: 新 LangChain 推荐放在 langchain_huggingface
# 我们做多级 fallback，确保不管你装的是哪个版本都能跑
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except ImportError:
        from langchain.embeddings import HuggingFaceEmbeddings  # 最旧版兜底

# 2. 导入我们本地LLM调用函数
from llm_local import call_local_llm

PERSIST_DIR = "./db/chroma_store"

# 你在 ingest.py 里用的是这个模型来做embedding
EMBED_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_retriever(top_k: int = 3):
    """
    打开已经持久化的 Chroma 向量库，并返回一个 retriever。
    retriever 会用 embedding 把查询变成向量，再做相似度搜索。
    """
    embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

    vs = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model
    )

    retriever = vs.as_retriever(search_kwargs={"k": top_k})
    return retriever


def build_prompt(user_question: str, rel_docs):
    """
    根据检索到的文档片段构造 Prompt，告诉 Qwen：
    - 推荐什么模块/传感器
    - 供电/接线注意什么
    - 怎么把数据上传到树莓派/平台
    - 必须基于来源文本，不要乱编
    - 输出时列出引用来源 (文件+页码)
    """

    context_blocks = []
    for d in rel_docs:
        src = f"{d.metadata.get('file')} p.{d.metadata.get('page')}"
        block = f"[{src}]\n{d.page_content}"
        context_blocks.append(block)

    context_text = "\n\n".join(context_blocks)

    prompt = f"""
你是IoT機器接続支援アシスタントです。
あなたの仕事は以下です：
1. ユーザの要求・利用シナリオに合うセンサ / モジュール / 通信方式を提案する。
2. 配線と電源(供給電圧・極性・最大電流など)の注意点を具体的に説明する。
3. Raspberry Pi やゲートウェイ(エッジノード)にどう接続し、どうやってデータを送るかを説明する。
4. 危険(過電圧・極性逆接など)があれば必ず警告する。
5. 回答は必ず下記「資料片段」の内容に基づくこと。資料に書いていない数値・仕様は勝手に作らない。
   情報が無い場合は「資料中に明記されていません」と言う。
6. 最後に「引用元」として、使った資料のファイル名とページ番号を列挙する。

【資料片段】
{context_text}

【ユーザの要求 / シナリオ】
{user_question}

日本語または中国語で丁寧に説明してください。
構成は次の4つのセクションで出力してください：
(1) 推奨デバイス / 方式
(2) 配線・電源の注意点
(3) Raspberry Pi / プラットフォームへの接続方法
(4) 引用元 (ファイル名とページ番号)
"""
    return prompt


def rag_answer(user_question: str):
    """
    对外暴露的主入口。
    步骤：
    1. 用 retriever 找到和问题最相关的文档片段
    2. 拼 prompt
    3. 调本地 Qwen (call_local_llm)
    4. 返回回答 + 证据
    """

    retriever = get_retriever(top_k=3)
    try:
    # 新版LangChain >=0.2.9 用 invoke()
        rel_docs = retriever.invoke(user_question)
    except AttributeError:
        # 旧版LangChain (<0.2.9) 用 get_relevant_documents()
        rel_docs = retriever.get_relevant_documents(user_question)

    prompt = build_prompt(user_question, rel_docs)
    answer_text = call_local_llm(prompt)

    # 准备证据（用于UI展示右侧原文、页码）
    evidence = [
        {
            "file": d.metadata.get("file"),
            "page": d.metadata.get("page")
        }
        for d in rel_docs
    ]

    raw_docs = [
        {
            "source": f"{d.metadata.get('file')} p.{d.metadata.get('page')}",
            "content": d.page_content
        }
        for d in rel_docs
    ]

    return {
        "answer": answer_text,
        "evidence": evidence,
        "raw_docs": raw_docs
    }


# 允许单独在命令行测试
if __name__ == "__main__":
    test_q = "室温を計測してRaspberry Piに送りたい。どのセンサを使えばいい？電源は何V必要？極性は？"
    result = rag_answer(test_q)

    print("=== 回答 ===")
    print(result["answer"])
    print("\n=== 証拠 ===")
    for ev in result["evidence"]:
        print(ev)
