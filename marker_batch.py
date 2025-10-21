from __future__ import annotations
import os
import sys
import time
import argparse
import threading
import queue
import re
from io import BytesIO
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Union, List, Tuple, Dict, Any
from collections import defaultdict
from math import ceil

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.output import text_from_rendered

PathLike = Union[str, os.PathLike]

# ==================== Torch device helpers ====================

def _normalize_device(device: Optional[str]) -> Optional[str]:
    if device is None:
        env_dev = os.environ.get("TORCH_DEVICE")
        if env_dev:
            fixed = _normalize_device(env_dev)
            os.environ["TORCH_DEVICE"] = fixed if fixed else ""
        return None
    d = str(device).strip().lower()
    if d in {"gpu", "cuda", "cuda:0", "cuda:1", "cuda:2"}:
        return "cuda"
    if d in {"cpu"}:
        return "cpu"
    return "cpu"

def _set_torch_device(device: Optional[str] = None):
    fixed = _normalize_device(device)
    if fixed is None:
        cur = os.environ.get("TORCH_DEVICE")
        if cur and _normalize_device(cur) != cur:
            os.environ["TORCH_DEVICE"] = _normalize_device(cur) or "cpu"
    else:
        os.environ["TORCH_DEVICE"] = fixed

# ==================== Marker config ====================

def _build_config_dict(
    *,
    output_format: str = "markdown",
    force_ocr: bool = False,
    strip_existing_ocr: bool = True,
    disable_image_extraction: bool = False,
    paginate_output: bool = True,
    page_range: Optional[str] = None,
) -> Dict[str, Any]:
    cfg = {
        "output_format": output_format,
        "force_ocr": bool(force_ocr),
        "strip_existing_ocr": bool(strip_existing_ocr),
        "disable_image_extraction": bool(disable_image_extraction),
        "paginate_output": bool(paginate_output),
    }
    if page_range:
        cfg["page_range"] = str(page_range)
    return cfg

def _new_converter(cfg_dict: Dict[str, Any]) -> PdfConverter:
    cfg = ConfigParser(cfg_dict)
    return PdfConverter(
        config=cfg.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=cfg.get_processors(),
        renderer=cfg.get_renderer(),
        llm_service=cfg.get_llm_service(),
    )

def iter_input_files(input_dir: PathLike, patterns: Iterable[str] = ("*.pdf",)) -> Iterable[Path]:
    in_dir = Path(input_dir)
    for pat in patterns:
        yield from in_dir.rglob(pat)

# ==================== image save utils ====================

def _to_pil_image(raw_obj):
    try:
        from PIL import Image
    except Exception:
        return None
    if "Image" in str(type(raw_obj)):
        return raw_obj
    try:
        if isinstance(raw_obj, (bytes, bytearray)):
            return Image.open(BytesIO(raw_obj))
        else:
            import numpy as np
            if isinstance(raw_obj, np.ndarray):
                return Image.fromarray(raw_obj)
    except Exception:
        return None
    return None

def _save_images_from_marker(images, out_img_dir: Path) -> Dict[str, str]:
    try:
        from PIL import Image  # noqa
    except Exception:
        print("[ERROR] Pillow not available -> skip image save", file=sys.stderr)
        return {}

    pending: List[Tuple[str, "Image.Image"]] = []

    for img in images or []:
        raw_name = None
        raw_obj = None
        if isinstance(img, tuple) and len(img) == 2:
            raw_name, raw_obj = img
        elif isinstance(img, dict):
            raw_name = img.get("name")
            raw_obj = img.get("image")

        if not raw_name or raw_obj is None:
            continue

        lname = str(raw_name).lower()
        # 跳过明显整页截图占位
        if lname in {"image0", "img_0000"}:
            continue

        pil_img = _to_pil_image(raw_obj)
        if pil_img is None:
            continue
        pending.append((str(raw_name), pil_img))

    if not pending:
        return {}

    out_img_dir.mkdir(parents=True, exist_ok=True)

    name_map: Dict[str, str] = {}
    for raw_name, pil_img in pending:
        base = raw_name.split(".")[0]
        out_path = out_img_dir / f"{base}.png"
        pil_img.save(out_path)
        name_map[base] = out_path.name

    return name_map

def _rewrite_md_image_refs(md_text: str, name_map: Dict[str, str], prefix: str = "") -> str:
    if not name_map:
        return md_text

    def _map_token(token: str) -> str | None:
        base = token.strip().split("/")[-1].split("\\")[-1]
        base = base.split(".")[0]
        if base in name_map:
            return f"{prefix}{name_map[base]}"
        return None

    # ![alt](token)
    def repl_md(m):
        alt = m.group(1)
        token = m.group(2)
        mapped = _map_token(token)
        return f"![{alt}]({mapped})" if mapped else m.group(0)

    md_text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_md, md_text)

    # <img src="token">
    def repl_html(m):
        token = m.group(1)
        mapped = _map_token(token)
        return f'<img src="{mapped}"' if mapped else m.group(0)

    md_text = re.sub(r'<img\s+[^>]*src=["\']([^"\']+)["\']', repl_html, md_text)

    return md_text

# ==================== text helpers & cleaning ====================

def _html_to_text(html: str) -> str:
    if not html:
        return ""
    html = html.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    html = re.sub(r"</p\s*>", "\n", html, flags=re.I)
    html = re.sub(r"</h[1-6]\s*>", "\n", html, flags=re.I)
    html = re.sub(r"</li\s*>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()

def _clean_line_text(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)

    page_patterns = [
        r'\bPage\s*\d+\s*of\s*\d+\b',
        r'第\s*\d+\s*页',
        r'^\s*\d+\s*/\s*\d+\s*$',
        r'^\s*\d{1,4}\s*$',
        r'^\s*[ivxlcdm]+\s*$',
    ]
    for pat in page_patterns:
        s = re.sub(pat, "", s, flags=re.IGNORECASE).strip()

    return s

def _looks_like_corporate_header(raw_line: str) -> bool:
    line = raw_line.strip()
    if not line:
        return False

    # 整行图片
    if re.match(r"^!\[[^\]]*\]\([^)]+\)$", line):
        return True

    low = line.lower()
    keywords_substr = [
        "www.",
        ".com",
        "weidm",            # weidmüller / weidmueller
        "klingenbergstraße",
        "detmold",
        "germany",
        "interface gmbh",
        "co. kg",
        "作成日",
        "カタログステータス",
        "catalog",
        "承認",
        "証明書",
        "適合証明書",
        "技術データ",
        "一般注文データ",
        "アクセサリ",
        "図に類似",
        "図面",
        "screenshot of",
        "connection to your pc",
    ]
    for kw in keywords_substr:
        if kw in low:
            return True

    # 地址行模式: 邮编+国家
    if re.search(r"\b\d{4,5}\b", low) and "germany" in low:
        return True

    # GmbH / Co. KG
    if re.search(r"\b(gmbh|co\.\s*kg)\b", low):
        return True

    return False

def _is_headerish_line(raw_line: str) -> bool:
    line = raw_line.strip()
    if not line:
        return True
    if _looks_like_corporate_header(line):
        return True
    low = line.lower()
    if re.match(r"^[a-z0-9._/-]+\.com\b", low):
        return True
    if ("germany" in low and re.search(r"\b\d{4,5}\b", low)):
        return True
    return False

def _strip_leading_header_block(lines: List[str]) -> List[str]:
    """
    从页首开始，连续剔除 headerish 行(logo/地址/URL/図に類似 等)，
    遇到第一行不是垃圾后，剩下全部保留。
    """
    keep_from = 0
    for idx, ln in enumerate(lines):
        if _is_headerish_line(ln):
            continue
        keep_from = idx
        break
    else:
        return []
    return lines[keep_from:]

def _line_should_survive_anywhere(raw_line: str) -> bool:
    """
    在整页范围内继续过滤纯垃圾行，比如 "www.weidmueller.com" 散落中间。
    """
    raw_line = raw_line.strip()
    if not raw_line:
        return False
    # 企业抬头 / logo caption / screenshot caption 都直接干掉
    if _looks_like_corporate_header(raw_line):
        return False
    return True

def _final_page_cleanup(page_text: str) -> str:
    """
    这是关键补丁。
    目标：
      1. 把整页文本按行分割
      2. 先做“页首剃头”(_strip_leading_header_block)
      3. 然后把剩余行再次逐行过滤(_line_should_survive_anywhere)
    返回干净版本
    """
    raw_lines = [ln.strip() for ln in page_text.splitlines()]
    # 1) 页首 header 块整体砍掉
    body_lines = _strip_leading_header_block(raw_lines)
    # 2) 对剩下的所有行做一遍企业垃圾过滤
    body_lines = [ln for ln in body_lines if _line_should_survive_anywhere(ln)]
    # 3) 合并 && 去掉重复的空白
    cleaned = "\n\n".join([ln for ln in body_lines if ln])
    cleaned = cleaned.strip()
    return cleaned

# ==================== header/footer candidate collection ====================

def _collect_header_footer_candidates(rendered: Any,
                                      top_frac: float = 0.4,
                                      bot_frac: float = 0.25):
    if isinstance(rendered, dict) and "pages" in rendered:
        pages_obj = rendered["pages"]
    else:
        pages_obj = rendered
    if not isinstance(pages_obj, list):
        pages_obj = []

    per_page_top: Dict[int, set[str]] = {}
    per_page_bot: Dict[int, set[str]] = {}
    N_pages = len(pages_obj)

    for page_idx, page_block in enumerate(pages_obj):
        page_poly = page_block.get("polygon", [])
        if page_poly:
            page_h = max(y for (_, y) in page_poly)
        else:
            page_h = 800.0

        top_cut = top_frac * page_h
        bot_cut = (1.0 - bot_frac) * page_h

        top_clean_set = set()
        bot_clean_set = set()

        for child in page_block.get("children", []) or []:
            child_html = child.get("html", "")
            full_text = _html_to_text(child_html)
            if not full_text:
                continue

            child_poly = child.get("polygon", [])
            if not child_poly:
                continue
            y_coords = [y for (_, y) in child_poly]
            if not y_coords:
                continue
            y_mid = 0.5 * (min(y_coords) + max(y_coords))

            for raw_line in full_text.splitlines():
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                clean_line = _clean_line_text(raw_line)
                if not clean_line:
                    continue

                if y_mid < top_cut:
                    top_clean_set.add(clean_line)
                elif y_mid > bot_cut:
                    bot_clean_set.add(clean_line)

        if top_clean_set:
            per_page_top[page_idx] = top_clean_set
        if bot_clean_set:
            per_page_bot[page_idx] = bot_clean_set

    return per_page_top, per_page_bot, N_pages

def _global_redundant_lines_majority(
    per_page_dict: Dict[int, set[str]],
    N_pages: int,
) -> set[str]:
    if N_pages <= 0:
        return set()
    need = ceil(N_pages / 2)
    counts: Dict[str, int] = defaultdict(int)
    for _, line_set in per_page_dict.items():
        for line in line_set:
            counts[line] += 1
    kill_set: set[str] = set()
    for line, cnt in counts.items():
        if cnt >= need:
            kill_set.add(line)
    return kill_set

# ==================== pagination split fallback ====================

def _split_by_markers(big_text: str) -> list[dict]:
    """
    用 {0}... 这种分页符切分大文本。
    如果没有，就整本当一页。
    """
    pattern = re.compile(r"^\{(\d+)\}[^\n]*\n", flags=re.MULTILINE)
    parts = pattern.split(big_text)

    if len(parts) < 3:
        return [
            {
                "page": 1,
                "text": big_text.strip()
            }
        ]

    out_pages: list[dict] = []
    for i in range(1, len(parts), 2):
        pageno_str = parts[i]
        body = parts[i + 1] if (i + 1) < len(parts) else ""
        try:
            logical_idx = int(pageno_str)
        except ValueError:
            continue
        body_clean = body.strip()
        if not body_clean:
            continue
        out_pages.append({
            "page": logical_idx + 1,
            "text": body_clean,
        })

    if not out_pages:
        out_pages = [
            {
                "page": 1,
                "text": big_text.strip()
            }
        ]

    return out_pages

# ==================== page chunk collector (core) ====================

def _collect_page_chunks_with_gprv(
    rendered: Any,
    pdf_name: str,
    full_md_text: str,
    *,
    top_frac: float = 0.4,
    bot_frac: float = 0.25,
) -> Dict[str, Any]:
    """
    产出:
    {
      "file": "...pdf",
      "total_pages": N,
      "pages": [
         {"page": 1, "text": "...clean..."},
         ...
      ]
    }

    清洗策略 (新版关键点)：
    - 无论是坐标分页还是 fallback 分页，最后都会跑 _final_page_cleanup()，
      强制剃掉页首的 logo/地址/URL/"図に類似"/www.weidmueller.com 等，并滤掉整页里任何纯垃圾行。
    """

    if isinstance(rendered, dict) and "pages" in rendered:
        pages_obj = rendered["pages"]
    else:
        pages_obj = rendered
    if not isinstance(pages_obj, list):
        pages_obj = []

    per_page_top, per_page_bot, N_pages = _collect_header_footer_candidates(
        rendered,
        top_frac=top_frac,
        bot_frac=bot_frac,
    )

    header_kill = _global_redundant_lines_majority(per_page_top, N_pages)
    footer_kill = _global_redundant_lines_majority(per_page_bot, N_pages)
    kill_lines = header_kill.union(footer_kill)

    def _should_keep_line_core(raw_line: str) -> bool:
        """
        这一层是早期筛选：主要在坐标分页路径里使用，
        先粗过滤明显 header/footer，再交给 _final_page_cleanup 做最后一刀。
        """
        raw_line = raw_line.strip()
        if not raw_line:
            return False
        # 如果在多数投票出来的抬头/页脚模板行里，扔
        clean_line = _clean_line_text(raw_line)
        if clean_line and clean_line in kill_lines:
            return False
        return True

    pages_list: list[dict] = []

    if pages_obj:
        # 坐标分页路径
        for idx, page_block in enumerate(pages_obj, start=1):
            collected_lines: List[str] = []

            # children
            for child in page_block.get("children", []) or []:
                child_html = child.get("html", "")
                child_text = _html_to_text(child_html)
                if not child_text:
                    continue
                for raw_line in child_text.splitlines():
                    if _should_keep_line_core(raw_line):
                        collected_lines.append(raw_line.strip())

            # fallback: page_block["html"]
            page_block_html = page_block.get("html", "")
            if page_block_html:
                block_text_guess = _html_to_text(page_block_html)
                if block_text_guess:
                    for raw_line in block_text_guess.splitlines():
                        if _should_keep_line_core(raw_line):
                            collected_lines.append(raw_line.strip())

            # join -> 再做最终强力清洗
            joined = "\n".join([l for l in collected_lines if l]).strip()
            cleaned_page = _final_page_cleanup(joined)

            if cleaned_page:
                pages_list.append({
                    "page": idx,
                    "text": cleaned_page,
                })

    # fallback：Marker没给坐标分页或我们没收集到
    if len(pages_list) == 0:
        pages_list = _split_by_markers(full_md_text)

        # 对 fallback 每页也做同样的最终强力清洗
        new_pages_list: list[dict] = []
        for p in pages_list:
            cleaned_page = _final_page_cleanup(p["text"])
            if cleaned_page:
                new_pages_list.append({
                    "page": p["page"],
                    "text": cleaned_page
                })
        pages_list = new_pages_list

    # 如果只有1页且像拼成大段，也尝试用 {0} ... 再切一次
    elif len(pages_list) == 1:
        resplit_pages = _split_by_markers(pages_list[0]["text"])
        if len(resplit_pages) > 1:
            new_pages_list: list[dict] = []
            for p in resplit_pages:
                cleaned_page = _final_page_cleanup(p["text"])
                if cleaned_page:
                    new_pages_list.append({
                        "page": p["page"],
                        "text": cleaned_page
                    })
            if new_pages_list:
                pages_list = new_pages_list

    result = {
        "file": pdf_name,
        "total_pages": len(pages_list),
        "pages": pages_list,
    }
    return result

# ==================== main sync API ====================

def convert_one(
    pdf_path: PathLike,
    output_dir: PathLike,
    *,
    device: Optional[str] = None,
    force_ocr: bool = False,
    strip_existing_ocr: bool = True,
    disable_image_extraction: bool = False,
    paginate_output: bool = True,
    page_range: Optional[str] = None,
) -> Path:
    """
    输出：
    - <stem>.md            原始 Marker markdown（人工看用）
    - <stem>_chunks.json   清洗后按页拆分文本（检索用）
    - <stem>_images/       抽出来的图片（如果有）
    """
    _set_torch_device(device)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg_dict = _build_config_dict(
        output_format="markdown",
        force_ocr=force_ocr,
        strip_existing_ocr=strip_existing_ocr,
        disable_image_extraction=disable_image_extraction,
        paginate_output=paginate_output,
        page_range=page_range,
    )
    converter = _new_converter(cfg_dict)

    pdf_path = Path(pdf_path)
    print(f"[INFO] Parsing: {pdf_path}")
    rendered = converter(str(pdf_path))

    md_text, _html_dump, images = text_from_rendered(rendered)

    # 生成干净的页文本
    chunks_meta = _collect_page_chunks_with_gprv(
        rendered,
        pdf_path.name,
        md_text,
        top_frac=0.4,
        bot_frac=0.25,
    )
    if not chunks_meta.get("pages"):
        chunks_meta = {
            "file": pdf_path.name,
            "total_pages": 1,
            "pages": [
                {
                    "page": 1,
                    "text": _final_page_cleanup(md_text.strip())
                }
            ]
        }

    # 图片导出 & Markdown内引用修正
    img_dir = out_dir / f"{pdf_path.stem}_images"
    name_map = _save_images_from_marker(images, img_dir)

    if not name_map:
        md_text = md_text.replace("![](image0)", "").replace("![](img_0000)", "")
    else:
        md_text = _rewrite_md_image_refs(md_text, name_map, prefix=f"{pdf_path.stem}_images/")

    # 写 <stem>.md（原始 Marker 文本）
    md_path = out_dir / f"{pdf_path.stem}.md"
    md_path.write_text(md_text, encoding="utf-8")

    # 写 <stem>_chunks.json（干净文本）
    import json
    json_path = out_dir / f"{pdf_path.stem}_chunks.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chunks_meta, f, ensure_ascii=False, indent=2)

    print(f"[OK] {pdf_path.name} -> {md_path.name} (pages={chunks_meta['total_pages']}, images={len(name_map)})")
    return md_path

# ==================== batch API ====================

def batch_convert(
    input_dir: PathLike,
    output_dir: PathLike,
    *,
    device: Optional[str] = None,
    force_ocr: bool = False,
    strip_existing_ocr: bool = True,
    disable_image_extraction: bool = False,
    paginate_output: bool = True,
    page_range: Optional[str] = None,
    patterns: Iterable[str] = ("*.pdf",),
) -> List[Path]:
    _set_torch_device(device)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = list(iter_input_files(input_dir, patterns=patterns))
    if not files:
        print(f"[WARN] No files matched in {input_dir} with patterns={patterns}")

    results: List[Path] = []

    try:
        from tqdm import tqdm  # type: ignore
        iterator = tqdm(files, desc="Marker parsing", unit="file")
    except Exception:
        iterator = files

    for f in iterator:
        try:
            md_path = convert_one(
                pdf_path=f,
                output_dir=out_dir,
                device=device,
                force_ocr=force_ocr,
                strip_existing_ocr=strip_existing_ocr,
                disable_image_extraction=disable_image_extraction,
                paginate_output=paginate_output,
                page_range=page_range,
            )
            results.append(md_path)
        except Exception as e:
            print(f"[WARN] Failed: {f} -> {e}", file=sys.stderr)

    print(f"[OK] generated: {len(results)} files -> {out_dir}")
    return results

# ==================== async API ====================

_thread_local = threading.local()

def _get_thread_local_converter(cfg_key: Tuple) -> PdfConverter:
    if not hasattr(_thread_local, "converters"):
        _thread_local.converters = {}
    store: Dict[Tuple, PdfConverter] = _thread_local.converters  # type: ignore
    if cfg_key not in store:
        cfg_dict = _build_config_dict(
            output_format=cfg_key[0],
            force_ocr=cfg_key[1],
            strip_existing_ocr=cfg_key[2],
            disable_image_extraction=cfg_key[3],
            paginate_output=cfg_key[4],
            page_range=cfg_key[5],
        )
        store[cfg_key] = _new_converter(cfg_dict)
    return store[cfg_key]

def _sync_convert_with_thread_local(
    file_path: Path,
    out_dir: Path,
    cfg_key: Tuple,
) -> Path:
    converter = _get_thread_local_converter(cfg_key)
    rendered = converter(str(file_path))
    md_text, _html, images = text_from_rendered(rendered)

    img_dir = out_dir / f"{file_path.stem}_images"
    name_map = _save_images_from_marker(images, img_dir)
    if name_map:
        md_text = _rewrite_md_image_refs(md_text, name_map, prefix=f"{file_path.stem}_images/")
    else:
        md_text = md_text.replace("![](image0)", "").replace("![](img_0000)", "")

    md_path = out_dir / (file_path.stem + ".md")
    md_path.write_text(md_text, encoding="utf-8")
    return md_path

async def aconvert_one(
    pdf_path: PathLike,
    output_dir: PathLike,
    *,
    device: Optional[str] = None,
    force_ocr: bool = False,
    strip_existing_ocr: bool = True,
    disable_image_extraction: bool = False,
    paginate_output: bool = True,
    page_range: Optional[str] = None,
    executor_workers: int = 1,
) -> Path:
    import asyncio
    _set_torch_device(device)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg_key = ("markdown", bool(force_ocr), bool(strip_existing_ocr),
               bool(disable_image_extraction), bool(paginate_output), page_range)

    loop = asyncio.get_running_loop()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=executor_workers) as ex:
        return await loop.run_in_executor(
            ex,
            _sync_convert_with_thread_local,
            Path(pdf_path),
            out_dir,
            cfg_key,
        )

async def abatch_convert(
    input_dir: PathLike,
    output_dir: PathLike,
    *,
    device: Optional[str] = None,
    force_ocr: bool = False,
    strip_existing_ocr: bool = True,
    disable_image_extraction: bool = False,
    paginate_output: bool = True,
    page_range: Optional[str] = None,
    patterns: Iterable[str] = ("*.pdf",),
    concurrency: int = 2,
) -> List[Path]:
    import asyncio
    _set_torch_device(device)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = list(iter_input_files(input_dir, patterns=patterns))
    cfg_key = ("markdown", bool(force_ocr), bool(strip_existing_ocr),
               bool(disable_image_extraction), bool(paginate_output), page_range)

    semaphore = asyncio.Semaphore(concurrency)
    results: List[Path] = []

    async def _task(fpath: Path) -> Optional[Path]:
        async with semaphore:
            try:
                return await aconvert_one(
                    fpath, out_dir,
                    device=device,
                    force_ocr=force_ocr,
                    strip_existing_ocr=strip_existing_ocr,
                    disable_image_extraction=disable_image_extraction,
                    paginate_output=paginate_output,
                    page_range=page_range,
                    executor_workers=1,
                )
            except Exception as e:
                print(f"[WARN] Failed: {fpath} -> {e}", file=sys.stderr)
                return None

    tasks = [_task(Path(f)) for f in files]
    for coro in asyncio.as_completed(tasks):
        r = await coro
        if r:
            results.append(r)
    print(f"[OK] generated: {len(results)} files -> {out_dir}")
    return results

# ==================== watcher service ====================

@dataclass
class ServiceConfig:
    input_dir: Path
    output_dir: Path
    device: Optional[str] = None
    force_ocr: bool = False
    strip_existing_ocr: bool = True
    disable_image_extraction: bool = False
    paginate_output: bool = True
    page_range: Optional[str] = None
    patterns: Tuple[str, ...] = ("*.pdf",)
    workers: int = 2
    poll_interval: float = 2.0
    dedup_seconds: float = 3.0

class MarkerAsyncService:
    """后台线程服务：轮询目录改动，自动跑 convert_one。"""

    def __init__(self, cfg: ServiceConfig):
        self.cfg = cfg
        self._stop = threading.Event()
        self._q: "queue.Queue[Optional[Path]]" = queue.Queue()
        self._seen: Dict[Path, float] = {}
        self._workers: List[threading.Thread] = []
        self._watcher: Optional[threading.Thread] = None

        _set_torch_device(cfg.device)
        self.cfg.output_dir.mkdir(parents=True, exist_ok=True)

    def start(self):
        if self._workers:
            return
        for i in range(max(1, self.cfg.workers)):
            t = threading.Thread(target=self._worker_loop, name=f"marker-worker-{i}", daemon=True)
            t.start()
            self._workers.append(t)
        self._watcher = threading.Thread(target=self._watch_loop, name="marker-watcher", daemon=True)
        self._watcher.start()
        print(f"[INFO] MarkerAsyncService started with {len(self._workers)} workers, watching: {self.cfg.input_dir}")

    def stop(self, wait: bool = True):
        self._stop.set()
        for _ in self._workers:
            self._q.put(None)
        if wait:
            for t in self._workers:
                t.join()
            if self._watcher:
                self._watcher.join()
        print("[INFO] MarkerAsyncService stopped.")

    def submit(self, file_path: PathLike):
        p = Path(file_path)
        if p.is_file():
            self._q.put(p)

    def _watch_loop(self):
        while not self._stop.is_set():
            now = time.time()
            for f in iter_input_files(self.cfg.input_dir, self.cfg.patterns):
                try:
                    st = f.stat()
                except FileNotFoundError:
                    continue
                mtime = st.st_mtime
                last = self._seen.get(f)
                self._seen[f] = mtime
                if last is None:
                    continue
                if mtime > last and (now - mtime) >= self.cfg.dedup_seconds:
                    self._q.put(f)

            primed = getattr(self, "_primed", False)
            if not primed:
                for f, mtime in list(self._seen.items()):
                    if (now - mtime) >= self.cfg.dedup_seconds:
                        self._q.put(f)
                setattr(self, "_primed", True)

            time.sleep(self.cfg.poll_interval)

    def _worker_loop(self):
        while not self._stop.is_set():
            try:
                item = self._q.get(timeout=0.5)
            except queue.Empty:
                continue
            if item is None:
                break

            fpath: Path = item
            try:
                convert_one(
                    pdf_path=fpath,
                    output_dir=self.cfg.output_dir,
                    device=self.cfg.device,
                    force_ocr=self.cfg.force_ocr,
                    strip_existing_ocr=self.cfg.strip_existing_ocr,
                    disable_image_extraction=self.cfg.disable_image_extraction,
                    paginate_output=self.cfg.paginate_output,
                    page_range=self.cfg.page_range,
                )
            except Exception as e:
                print(f"[WARN] Failed: {fpath} -> {e}", file=sys.stderr)
            finally:
                self._q.task_done()

# ==================== CLI ====================

def _add_common_args(ap: argparse.ArgumentParser):
    ap.add_argument("-i", "--input_dir", required=True, help="输入目录")
    ap.add_argument("-o", "--output_dir", required=True, help="输出目录")
    ap.add_argument("--device", choices=["cuda", "cpu"], default=None, help="Torch 设备；默认自动")
    ap.add_argument("--force_ocr", action="store_true", help="全量 OCR（更稳，但更慢）")
    ap.add_argument("--strip_existing_ocr", action="store_true", default=True, help="移除已有 OCR 并重做")
    ap.add_argument("--no-strip_existing_ocr", dest="strip_existing_ocr", action="store_false")
    ap.add_argument("--disable_image_extraction", action="store_true", help="不导出图片")
    ap.add_argument("--paginate_output", action="store_true", default=True, help="在输出中加入分页标记")
    ap.add_argument("--no-paginate_output", dest="paginate_output", action="store_false")
    ap.add_argument("--page_range", default=None, help='页范围，如 "0,5-10,20"')
    ap.add_argument("--patterns", nargs="+", default=["*.pdf"], help="通配符，默认 *.pdf")

def main():
    parser = argparse.ArgumentParser(description="Marker 批量解析（支持异步监听）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ap_once = sub.add_parser("once", help="一次性批量解析")
    _add_common_args(ap_once)

    ap_watch = sub.add_parser("watch", help="异步监听目录并解析")
    _add_common_args(ap_watch)
    ap_watch.add_argument("--workers", type=int, default=2, help="工作线程数（建议从 1 或 2 起）")
    ap_watch.add_argument("--poll_interval", type=float, default=2.0, help="轮询间隔秒")
    ap_watch.add_argument("--dedup_seconds", type=float, default=3.0, help="文件稳定等待秒")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if args.cmd == "once":
        paths = batch_convert(
            input_dir=input_dir,
            output_dir=output_dir,
            device=args.device,
            force_ocr=args.force_ocr,
            strip_existing_ocr=args.strip_existing_ocr,
            disable_image_extraction=args.disable_image_extraction,
            paginate_output=args.paginate_output,
            page_range=args.page_range,
            patterns=tuple(args.patterns),
        )
        print(f"[OK] generated: {len(paths)} files -> {output_dir}")

    elif args.cmd == "watch":
        cfg = ServiceConfig(
            input_dir=input_dir,
            output_dir=output_dir,
            device=args.device,
            force_ocr=args.force_ocr,
            strip_existing_ocr=args.strip_existing_ocr,
            disable_image_extraction=args.disable_image_extraction,
            paginate_output=args.paginate_output,
            page_range=args.page_range,
            patterns=tuple(args.patterns),
            workers=args.workers,
            poll_interval=args.poll_interval,
            dedup_seconds=args.dedup_seconds,
        )
        svc = MarkerAsyncService(cfg)
        svc.start()
        try:
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            svc.stop(wait=True)

if __name__ == "__main__":
    main()
