# marker_run.py
# 只解析新增/更新过的 PDF，不重复处理

import os
from pathlib import Path
from multiprocessing import freeze_support

# -------- 设备相关 / 环境准备 --------
def pick_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"

def ensure_env_ok():
    # 清理无效设备名，比如有人设了 TORCH_DEVICE=gpu
    if os.environ.get("TORCH_DEVICE", "").lower() == "gpu":
        os.environ.pop("TORCH_DEVICE", None)

    # 可选的小优化，减少并发噪声
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    os.environ.setdefault("OMP_NUM_THREADS", "1")

    # Pillow 检查（Marker 导出图片时会用到）
    try:
        import PIL  # noqa: F401
    except Exception:
        raise SystemExit("[ERROR] 缺少依赖：pillow。请先运行: pip install pillow")

# -------- 核心逻辑：仅处理未解析/需要重新解析的 PDF --------
def needs_parse(pdf_path: Path, output_dir: Path) -> Path | None:
    """
    决定这个 pdf 是否需要解析。
    返回将要写入的 md 路径；如果不需要解析则返回 None。

    规则：
    - 目标 md 文件不存在  => 需要解析
    - 目标 md 文件存在但比 pdf 旧 => 需要解析
    - 否则跳过
    """
    md_path = output_dir / f"{pdf_path.stem}.md"
    if not md_path.exists():
        return md_path

    pdf_mtime = pdf_path.stat().st_mtime
    md_mtime = md_path.stat().st_mtime
    if md_mtime < pdf_mtime:
        # PDF 更新过，重新解析
        return md_path

    # 否则说明已经是最新，跳过
    return None

def walk_pdfs(input_dir: Path) -> list[Path]:
    """递归收集所有 .pdf / .PDF 文件"""
    pdfs: list[Path] = []
    for ext in ("*.pdf", "*.PDF"):
        pdfs.extend(input_dir.rglob(ext))
    return sorted(set(pdfs))

# -------- 主执行流程 --------
def run():
    from marker_batch import convert_one  # 延迟导入，避免 multiprocessing spawn 时重复副作用

    # 你自己的路径，可以改
    INPUT_DIR = Path(r"F:\KeyWordSystem\data")
    OUTPUT_DIR = Path(r"F:\KeyWordSystem\output")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ensure_env_ok()
    device = pick_device()
    print(f"[INFO] using device: {device}")
    print(f"[INFO] scanning PDFs under {INPUT_DIR}")

    all_pdfs = walk_pdfs(INPUT_DIR)
    if not all_pdfs:
        print("[WARN] 没找到任何 PDF")
        return

    # 1. 过滤需要处理的PDF
    to_process: list[Path] = []
    for pdf in all_pdfs:
        md_target = needs_parse(pdf, OUTPUT_DIR)
        if md_target is not None:
            to_process.append(pdf)

    if not to_process:
        print("[INFO] 没有新增或更新的 PDF，全部都是最新的 ✅")
    else:
        print(f"[INFO] 本次需要解析的文件数: {len(to_process)}")
        for p in to_process:
            print(f"    - {p}")

    # 2. 逐个解析需要处理的 PDF（使用 convert_one）
    parsed_md_paths: list[Path] = []
    for pdf in to_process:
        try:
            md_path = convert_one(
                pdf_path=pdf,
                output_dir=OUTPUT_DIR,
                device=device,
                force_ocr=False,
                strip_existing_ocr=True,
                disable_image_extraction=False,
                paginate_output=True,
                page_range=None,
            )
            parsed_md_paths.append(md_path)
        except Exception as e:
            print(f"[ERROR] 解析失败 {pdf.name}: {e}")

    # 3. 汇总所有（包含之前就存在的）
    final_md_files: list[Path] = []
    for pdf in all_pdfs:
        md_file = OUTPUT_DIR / f"{pdf.stem}.md"
        if md_file.exists():
            final_md_files.append(md_file)

    print(f"[OK] markdown files (total): {len(final_md_files)}")
    for md in final_md_files:
        stem = md.stem
        img_dir = OUTPUT_DIR / f"{stem}_images"
        imgs = list(img_dir.glob("*.png")) if img_dir.exists() else []
        print(f"    - {md.name}  | images: {len(imgs)}  | images_dir: {img_dir if imgs else '—'}")

if __name__ == "__main__":
    # Windows 多进程安全要求
    freeze_support()
    run()
