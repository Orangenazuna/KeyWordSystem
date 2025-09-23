# app.py —— Original Framework (config-based)，自动运行版（无需命令行参数）
import os, json, subprocess, sys
from pathlib import Path
from typing import List, Dict, Any
from rules import extract_spec  # 你自己的规则抽取（AI 兜底后续再接）

# ====== 只改这里就能跑 ======
ROOT        = Path(__file__).resolve().parent
PDF_PATH    = ROOT / "data" / "mcp9700.pdf"          # ← 指定要解析的 PDF
OUT_DIR     = ROOT / "output" / "mcp9700"            # ← 输出目录
CACHE_DIR   = ROOT / ".dolphin_cache"                # ← Dolphin 中间产物
MAX_BATCH   = 8                                      # 原生框架建议先 8
# =================================

# Dolphin 仓库与配置（按原生框架）
DOLPHIN_REPO   = (ROOT / "Dolphin").resolve()
DOLPHIN_CONFIG = (DOLPHIN_REPO / "config" / "Dolphin.yaml").resolve()
MODE           = "config"  # 固定原生框架

# （可选）尝试读取 YAML，做“tokenizer/ckpt”文件存在性检查，便于提前发现配置错误
def _soft_check_yaml_model_paths():
    try:
        import yaml  # pip install pyyaml（没有也不影响运行）
        y = yaml.safe_load(DOLPHIN_CONFIG.read_text(encoding="utf-8"))
        # 常见键位（不同仓库稍有差异，这里尽量兼容）
        model_args = (y.get("model_args") or y.get("model") or {})
        maybe_paths = []
        for k in ("tokenizer_path", "tokenizer_file", "ckpt_path", "checkpoint", "model_path"):
            v = model_args.get(k)
            if isinstance(v, str):
                maybe_paths.append(v)
        missing = [p for p in maybe_paths if not Path(p).expanduser().exists()]
        if missing:
            print("[WARN] Dolphin.yaml 里的以下模型/分词器路径不存在：")
            for p in missing:
                print("   -", p)
            print("      → 请把它们改成你本地实际存在的绝对路径（例如 F:\\KeyWordSystem\\Dolphin\\...）")
    except Exception as e:
        print("[INFO] 跳过 YAML 自检（", e, ")")

def _preflight() -> None:
    assert (DOLPHIN_REPO / "demo_page.py").exists(), f"找不到 {DOLPHIN_REPO/'demo_page.py'}"
    assert DOLPHIN_CONFIG.exists(), f"找不到配置文件 {DOLPHIN_CONFIG}"
    assert PDF_PATH.exists(), f"找不到PDF：{PDF_PATH}"
    _soft_check_yaml_model_paths()

def run_dolphin_config(input_path: Path, save_dir: Path, max_batch: int = 8) -> List[str]:
    """调用 Dolphin 的原生整页解析，返回生成的 JSON 列表"""
    input_path = input_path.resolve()
    save_dir   = save_dir.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, str(DOLPHIN_REPO / "demo_page.py"),
        "--config", str(DOLPHIN_CONFIG),
        "--input_path", str(input_path),
        "--save_dir", str(save_dir),
        "--max_batch_size", str(max_batch),
    ]

    print(f"[DEBUG] RUN: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("[DEBUG] Dolphin STDOUT >>>"); print(res.stdout)
    print("[DEBUG] Dolphin STDERR >>>"); print(res.stderr)
    if res.returncode != 0:
        raise RuntimeError(f"Dolphin(config) 运行失败，returncode={res.returncode}")

    jsons = sorted(str(p) for p in save_dir.rglob("*.json"))
    print(f"[DEBUG] JSON found: {len(jsons)}")
    if not jsons:
        print("[WARN] 没找到 JSON，列出 save_dir 内容：")
        for p in save_dir.rglob("*"):
            print("   ", p)
    return jsons

def load_blocks(json_files: List[str]) -> List[Dict[str, Any]]:
    """把 Dolphin page-level JSON 适配成统一块：page/bbox/type/content"""
    blocks: List[Dict[str, Any]] = []
    for jf in json_files:
        try:
            data = json.loads(Path(jf).read_text(encoding="utf-8", errors="ignore"))
        except Exception as e:
            print(f"[WARN] 读取 {jf} 失败：{e}")
            continue
        page_no  = int(data.get("page_number") or data.get("page") or 1)
        elements = data.get("elements") or data.get("items") or []
        for el in elements:
            etype = (el.get("type") or el.get("category") or "text").lower()
            box   = el.get("bbox") or el.get("box") or el.get("position") or [0,0,0,0]
            if etype == "table":
                content = el.get("markdown") or el.get("table_markdown") or el.get("text") or ""
            elif etype in ("formula","equation","math"):
                content = el.get("latex") or el.get("text") or ""
                etype   = "formula"
            else:
                content = el.get("text") or el.get("content") or ""
                etype   = "text"
            blocks.append({"page": page_no, "bbox": _bbox(box), "type": etype, "content": content})
    print(f"[DEBUG] Blocks loaded: {len(blocks)}")
    return blocks

def _bbox(b):
    try:
        return [float(b[0]), float(b[1]), float(b[2]), float(b[3])]
    except Exception:
        return [0.0, 0.0, 0.0, 0.0]

def save_spec(spec: Dict[str, Any], out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "semar_spec.json"
    out_file.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Saved → {out_file}")

def main():
    print(f"[INFO] MODE = {MODE} (config-based)")
    print(f"[INFO] PDF  = {PDF_PATH}")
    print(f"[INFO] OUT  = {OUT_DIR}")
    _preflight()

    json_files = run_dolphin_config(PDF_PATH, CACHE_DIR, MAX_BATCH)
    if not json_files:
        print("[ERROR] 未生成 JSON，无法继续。")
        return
    blocks = load_blocks(json_files)
    if not blocks:
        print("[ERROR] 未加载到块数据。")
        return
    spec = extract_spec(blocks)   # 使用你的 rules.py
    save_spec(spec, OUT_DIR)

if __name__ == "__main__":
    main()
