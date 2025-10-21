"""
解析PDF文件，转换成markdown，以及图片。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Paths
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"
DOLPHIN_MD_DIR = ROOT / ".dolphin_cache" / "markdown"
RECOG_JSON_DIR = ROOT / ".dolphin_cache" / "recognition_json"


# Normalization
MICRO_MAP = {"μ": "µ"}
OHM_MAP = {"ohm": "Ω", "Ω": "Ω"}


def to_halfwidth(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def normalize_units(s: str) -> str:
    t = s
    for src, dst in MICRO_MAP.items():
        t = t.replace(src, dst)
    for src, dst in OHM_MAP.items():
        t = t.replace(src, dst)
    return t


def clean_text(s: str) -> str:
    return normalize_units(to_halfwidth(s)).strip()


COLON_PATTERN = re.compile(r"[:\uFF1A]")  # ASCII ':' or full-width '：'


def split_key_value(line: str) -> Tuple[str, str]:
    m = COLON_PATTERN.search(line)
    if not m:
        return line.strip(), ""
    left = line[: m.start()]
    right = line[m.end() :]
    return left.strip(), right.strip()


# Aliases (schema mapping)
CANONICAL_KEYS: Dict[str, List[str]] = {
    "vcc": [
        "vcc",
        "vdd",
        "vin",
        "supply voltage",
        "operating voltage",
        "input voltage",
        "电源电压",
        "供电电压",
    ],
    "i_supply": [
        "supply current",
        "operating current",
        "current consumption",
        "iquiescent",
        "iq",
        "电源电流",
        "静态电流",
    ],
    "temp_range": [
        "temperature range",
        "operating temperature",
        "ambient temperature",
        "工作温度",
        "温度范围",
        "环境温度",
    ],
}


def _norm_key(s: str) -> str:
    s2 = clean_text(s).lower()
    return " ".join("".join(ch for ch in s2 if ch.isalnum() or ch.isspace()).split())


def map_key(raw_key: str) -> Tuple[Optional[str], Optional[str]]:
    k = _norm_key(raw_key)
    for canonical, aliases in CANONICAL_KEYS.items():
        for a in aliases:
            if k == _norm_key(a):
                return canonical, a
    return None, None


# Markdown parsing
class Heading:
    def __init__(self, level: int, text: str, line: int):
        self.level = level
        self.text = text
        self.line = line


class KeyValue:
    def __init__(self, key: str, value: str, line: int, section: Optional[str]):
        self.key = key
        self.value = value
        self.line = line
        self.section = section


def parse_markdown(md_text: str) -> List[object]:
    items: List[object] = []
    current_section: Optional[str] = None
    for idx, raw in enumerate(md_text.splitlines(), start=1):
        line = clean_text(raw)
        if not line:
            continue
        if line.startswith("#"):
            lvl = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            current_section = text
            items.append(Heading(level=lvl, text=text, line=idx))
            continue
        if line.startswith("|") and line.endswith("|"):
            continue  # M1: skip tables
        if COLON_PATTERN.search(line):
            k, v = split_key_value(line)
            if k and v:
                items.append(KeyValue(key=k, value=v, line=idx, section=current_section))
    return items


# Value parsing
def parse_value(text: str) -> Dict[str, object]:
    t = clean_text(text)
    m = re.match(
        r"^([+\-]?\d+(?:\.\d+)?)\s*([^\d\s]*)\s*(?:[~\-–—]|\s+to\s+)\s*([+\-]?\d+(?:\.\d+)?)\s*([^\d\s]*)$",
        t,
        flags=re.I,
    )
    if m:
        a, unit_a, b, unit_b = m.groups()
        unit = unit_a or unit_b or ""
        return {"min": float(a), "max": float(b), "unit": unit, "raw": text}

    m2 = re.match(r"^([+\-]?\d+(?:\.\d+)?)(?:\s*([a-zA-Zµ°Ω%]+))?$", t)
    if m2:
        val, unit = m2.groups()
        return {"value": float(val), "unit": unit or "", "raw": text}

    m3 = re.search(r"([+\-]?\d+(?:\.\d+)?)", t)
    if m3:
        val = float(m3.group(1))
        unit = t[m3.end():].strip()
        unit = unit if unit and len(unit) <= 5 else ""
        return {"value": val, "unit": unit, "raw": text}

    return {"raw": text}


# Validators
def _pick_value(p: Dict[str, object]):
    if "value" in p:
        try:
            return float(p["value"])  # type: ignore[arg-type]
        except Exception:
            return None
    if "min" in p and "max" in p:
        try:
            return (float(p["min"]) + float(p["max"])) / 2.0  # type: ignore[arg-type]
        except Exception:
            return None
    return None


def validate_params(params: List[Dict[str, object]]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    issues: List[Dict[str, object]] = []
    updated: List[Dict[str, object]] = []
    for p in params:
        key = p.get("key")
        unit = (p.get("unit") or "").strip()
        conf = float(p.get("confidence") or 0.6)
        ok = True
        if key == "vcc":
            val = _pick_value(p)
            if val is None or not (1.0 <= val <= 12.0):
                ok = False
                issues.append({"key": key, "issue": "vcc_out_of_range", "detail": p})
        elif key == "i_supply":
            val = _pick_value(p)
            if val is None or val < 0:
                ok = False
                issues.append({"key": key, "issue": "i_supply_negative", "detail": p})
        elif key == "temp_range":
            tmin = p.get("min")
            tmax = p.get("max")
            if tmin is None or tmax is None or tmin < -200 or tmax > 300:
                ok = False
                issues.append({"key": key, "issue": "temp_range_invalid", "detail": p})
            else:
                if not (-55 <= float(tmin) and float(tmax) <= 150):
                    ok = False
                    issues.append({"key": key, "issue": "temp_range_outside_common", "detail": p})
        if unit and unit not in {"V", "A", "mA", "µA", "°C", "Ω", "%", "kHz", "Hz"}:
            issues.append({"key": key, "issue": "unknown_unit", "unit": unit})
        if ok and conf < 0.8:
            p["confidence"] = 0.8
        updated.append(p)
    return updated, issues


# Emitters
def write_json(doc: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def write_yaml(device: str, specs: List[Dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append(f"device: {device}")
    lines.append("specs:")
    for s in specs:
        key = s.get("key", "")
        lines.append(f"  - key: {key}")
        for fld in ("value", "unit", "min", "max", "confidence"):
            if fld in s and s[fld] not in (None, ""):
                lines.append(f"    {fld}: {s[fld]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# Batch helpers
def discover_inputs(data_dir: Path) -> List[Tuple[str, Optional[Path], Optional[Path]]]:
    stems: Dict[str, Dict[str, Path]] = {}
    for p in data_dir.glob("*.*"):
        if p.suffix.lower() not in {".pdf", ".md"}:
            continue
        stems.setdefault(p.stem, {})[p.suffix.lower()] = p
    out: List[Tuple[str, Optional[Path], Optional[Path]]] = []
    for stem, mp in stems.items():
        out.append((stem, mp.get(".pdf"), mp.get(".md")))
    return out


def process_markdown_text(stem: str, md_text: str) -> Dict[str, object]:
    items = parse_markdown(md_text)
    params: List[Dict[str, object]] = []
    issues: List[Dict[str, object]] = []
    for it in items:
        if isinstance(it, KeyValue):
            canonical, _ = map_key(it.key)
            if not canonical:
                continue
            val = parse_value(it.value)
            param: Dict[str, object] = {
                "key": canonical,
                "confidence": 0.6,
                "raw": it.value,
                "source": {"line": it.line, "section": it.section},
            }
            param.update(val)
            params.append(param)
    params, rule_issues = validate_params(params)
    issues.extend(rule_issues)
    doc = {"device": stem, "params": params, "meta": {"issues": issues}}
    return doc


# Dolphin helpers
DOLPHIN_REPO = (ROOT / "Dolphin").resolve()
DOLPHIN_CONFIG = (DOLPHIN_REPO / "config" / "Dolphin.yaml").resolve()
CACHE_DIR = ROOT / ".dolphin_cache"
MAX_BATCH = 1


def _soft_check_yaml_model_paths():
    try:
        import yaml  # optional

        y = yaml.safe_load(DOLPHIN_CONFIG.read_text(encoding="utf-8"))
        model_args = (y.get("model_args") or y.get("model") or {})
        maybe_paths = []
        for k in ("tokenizer_path", "tokenizer_file", "ckpt_path", "checkpoint", "model_path"):
            v = model_args.get(k)
            if isinstance(v, str):
                maybe_paths.append(v)
        missing = [p for p in maybe_paths if not Path(p).expanduser().exists()]
        if missing:
            print("[WARN] Missing paths in Dolphin.yaml:")
            for p in missing:
                print("   -", p)
    except Exception as e:
        print("[INFO] Skip YAML self-check:", e)


def run_dolphin_config(
    input_path: Path,
    save_dir: Path,
    max_batch: int = MAX_BATCH,
    timeout_sec: int = 0,
    stream: bool = True,
) -> List[str]:
    input_path = input_path.resolve()
    save_dir = save_dir.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)

    # Preflight torch info
    try:
        import torch  # type: ignore
        print(
            f"[DEBUG] Torch {getattr(torch, '__version__', 'unknown')} CUDA? {torch.cuda.is_available()} CUDA {getattr(torch.version, 'cuda', None)}"
        )
        if torch.cuda.is_available():
            try:
                print(f"[DEBUG] GPU: {torch.cuda.get_device_name(0)}")
            except Exception:
                pass
    except Exception as e:
        print(f"[DEBUG] Torch import failed: {e}")

    env = os.environ.copy()
    env.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:64,expandable_segments:True")
    env.setdefault("TOKENIZERS_PARALLELISM", "false")
    env.setdefault("DOLPHIN_FORCE_DTYPE", "float16")

    cmd = [
        sys.executable,
        str(DOLPHIN_REPO / "demo_page.py"),
        "--config",
        str(DOLPHIN_CONFIG),
        "--input_path",
        str(input_path),
        "--save_dir",
        str(save_dir),
        "--max_batch_size",
        str(max_batch),
    ]
    print(f"[DEBUG] RUN: {' '.join(cmd)}")

    if stream:
        try:
            with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env,
            ) as p:
                if p.stdout is not None:
                    for line in p.stdout:
                        print("[DOLPHIN]", line.rstrip())
                if timeout_sec:
                    try:
                        p.wait(timeout=timeout_sec)
                    except subprocess.TimeoutExpired:
                        p.kill()
                        print("[WARN] Dolphin timeout, killed.")
        except Exception as e:
            print(f"[ERROR] Dolphin launch failed: {e}")
    else:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec or None, env=env)
        if res.stdout:
            print("[DEBUG] Dolphin STDOUT >>>\n" + res.stdout)
        if res.stderr:
            print("[DEBUG] Dolphin STDERR >>>\n" + res.stderr)
        if res.returncode != 0:
            raise RuntimeError(f"Dolphin returned {res.returncode}")

    jsons = sorted(str(p) for p in save_dir.rglob("*.json"))
    print(f"[DEBUG] JSON found: {len(jsons)}")
    return jsons


def _load_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def _synthesize_md_from_recognition(rec_json: Path) -> Optional[Path]:
    data = _load_json(rec_json)
    if not data:
        return None
    elements = data.get("elements") or data.get("items") or []
    lines: List[str] = []
    for el in elements:
        etype = (el.get("type") or el.get("category") or "text").lower()
        if etype == "table":
            md = el.get("markdown") or el.get("table_markdown")
            if md:
                lines.append(md)
        else:
            txt = el.get("text") or el.get("content")
            if txt:
                lines.append(str(txt).strip())
    stem = rec_json.stem
    md_path = DOLPHIN_MD_DIR / f"{stem}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    return md_path


def ensure_markdown_from_pdf(stem: str, pdf_path: Path, *, timeout_sec: int = 0, max_batch: int = MAX_BATCH) -> Optional[Path]:
    md_cache = DOLPHIN_MD_DIR / f"{stem}.md"
    if md_cache.exists():
        return md_cache
    try:
        _soft_check_yaml_model_paths()
        run_dolphin_config(pdf_path, CACHE_DIR, max_batch=max_batch, timeout_sec=timeout_sec, stream=True)
    except Exception:
        pass
    if md_cache.exists():
        return md_cache
    rec_json = RECOG_JSON_DIR / f"{stem}.json"
    if rec_json.exists():
        return _synthesize_md_from_recognition(rec_json)
    for c in CACHE_DIR.rglob(f"{stem}.json"):
        synth = _synthesize_md_from_recognition(c)
        if synth and synth.exists():
            return synth
    return None


def _copy_dolphin_figures(stem: str, out_dir: Path) -> int:
    src_dir = DOLPHIN_MD_DIR / "figures"
    if not src_dir.exists():
        return 0
    dst_dir = out_dir / "figures"
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in src_dir.glob(f"{stem}_*.png"):
        try:
            shutil.copy2(p, dst_dir / p.name)
            count += 1
        except Exception:
            pass
    return count


# Batch runner with progress prints
def run_batch(use_dolphin_cache: bool = True, persist_md: bool = False, use_dolphin_when_missing: bool = True, *, dolphin_timeout: int = 0, dolphin_batch: int = MAX_BATCH, only: Optional[str] = None) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    all_log_lines: List[str] = []
    for stem, pdf, md in discover_inputs(DATA_DIR):
        if only and stem != only:
            continue
        try:
            log_lines: List[str] = []
            log_lines.append(f"== {stem} ==")
            print(f"[RUN] Processing: {stem}")
            md_path_data = DATA_DIR / f"{stem}.md"
            md_path_cache = DOLPHIN_MD_DIR / f"{stem}.md"
            if md_path_data.exists():
                print(f"[SRC] data/{stem}.md")
                text = md_path_data.read_text(encoding="utf-8", errors="ignore")
                doc = process_markdown_text(stem, text)
                out_dir = OUT_DIR / stem
                out_dir.mkdir(parents=True, exist_ok=True)
                write_json(doc, out_dir / f"{stem}.json")
                specs: List[Dict[str, object]] = []
                for p in doc["params"]:  # type: ignore[index]
                    specs.append({
                        "key": p.get("key"),
                        **({"value": p["value"]} if "value" in p else {}),
                        **({"min": p["min"], "max": p["max"]} if "min" in p and "max" in p else {}),
                        "unit": p.get("unit", ""),
                        "confidence": p.get("confidence", 0.6),
                    })
                write_yaml(stem, specs, out_dir / f"{stem}.yaml")
                try:
                    (out_dir / "source.md").write_text(text, encoding="utf-8")
                except Exception as e:
                    log_lines.append(f"WARN write source.md failed: {e}")
                copied = _copy_dolphin_figures(stem, out_dir)
                if copied:
                    log_lines.append(f"Copied figures: {copied} files")
                log_lines.append(f"Processed markdown: {md_path_data}")
            elif use_dolphin_cache and md_path_cache.exists():
                print(f"[SRC] cache md: .dolphin_cache/markdown/{stem}.md")
                text = md_path_cache.read_text(encoding="utf-8", errors="ignore")
                doc = process_markdown_text(stem, text)
                out_dir = OUT_DIR / stem
                out_dir.mkdir(parents=True, exist_ok=True)
                write_json(doc, out_dir / f"{stem}.json")
                specs: List[Dict[str, object]] = []
                for p in doc["params"]:  # type: ignore[index]
                    specs.append({
                        "key": p.get("key"),
                        **({"value": p["value"]} if "value" in p else {}),
                        **({"min": p["min"], "max": p["max"]} if "min" in p and "max" in p else {}),
                        "unit": p.get("unit", ""),
                        "confidence": p.get("confidence", 0.6),
                    })
                write_yaml(stem, specs, out_dir / f"{stem}.yaml")
                try:
                    (out_dir / "source.md").write_text(text, encoding="utf-8")
                except Exception as e:
                    log_lines.append(f"WARN write source.md failed: {e}")
                copied = _copy_dolphin_figures(stem, out_dir)
                if copied:
                    log_lines.append(f"Copied figures: {copied} files")
                log_lines.append(f"Processed dolphin-cache markdown: {md_path_cache}")
                if persist_md:
                    try:
                        (DATA_DIR / f"{stem}.md").write_text(text, encoding="utf-8")
                        log_lines.append(f"Persisted markdown to data/: {DATA_DIR / (str(stem)+'.md')}")
                    except Exception as e:
                        log_lines.append(f"WARN persist_md failed: {e}")
            elif use_dolphin_when_missing and pdf and pdf.exists():
                print(f"[SRC] generate md for: {stem}")
                md_gen = ensure_markdown_from_pdf(stem, pdf, timeout_sec=dolphin_timeout, max_batch=dolphin_batch)
                if md_gen and md_gen.exists():
                    print(f"[SRC] generated md: {md_gen.name}")
                    text = md_gen.read_text(encoding="utf-8", errors="ignore")
                    doc = process_markdown_text(stem, text)
                    out_dir = OUT_DIR / stem
                    out_dir.mkdir(parents=True, exist_ok=True)
                    write_json(doc, out_dir / f"{stem}.json")
                    specs: List[Dict[str, object]] = []
                    for p in doc["params"]:  # type: ignore[index]
                        specs.append({
                            "key": p.get("key"),
                            **({"value": p["value"]} if "value" in p else {}),
                            **({"min": p["min"], "max": p["max"]} if "min" in p and "max" in p else {}),
                            "unit": p.get("unit", ""),
                            "confidence": p.get("confidence", 0.6),
                        })
                    write_yaml(stem, specs, out_dir / f"{stem}.yaml")
                    try:
                        (out_dir / "source.md").write_text(text, encoding="utf-8")
                    except Exception as e:
                        log_lines.append(f"WARN write source.md failed: {e}")
                    copied = _copy_dolphin_figures(stem, out_dir)
                    if copied:
                        log_lines.append(f"Copied figures: {copied} files")
                    log_lines.append(f"Processed dolphin-generated markdown: {md_gen}")
                    if persist_md:
                        try:
                            (DATA_DIR / f"{stem}.md").write_text(text, encoding="utf-8")
                            log_lines.append(f"Persisted markdown to data/: {DATA_DIR / (str(stem)+'.md')}")
                        except Exception as e:
                            log_lines.append(f"WARN persist_md failed: {e}")
                else:
                    print(f"[SRC] no md generated; writing placeholder for {stem}")
                    out_dir = OUT_DIR / stem
                    out_dir.mkdir(parents=True, exist_ok=True)
                    doc = {"device": stem, "params": [], "meta": {"issues": [{"issue": "markdown_missing", "pdf": str(pdf) if pdf else None}]}}
                    write_json(doc, out_dir / f"{stem}.json")
                    write_yaml(stem, [], out_dir / f"{stem}.yaml")
            else:
                print(f"[SRC] no md; writing placeholder for {stem}")
                out_dir = OUT_DIR / stem
                out_dir.mkdir(parents=True, exist_ok=True)
                doc = {"device": stem, "params": [], "meta": {"issues": [{"issue": "markdown_missing", "pdf": str(pdf) if pdf else None}]}}
                write_json(doc, out_dir / f"{stem}.json")
                write_yaml(stem, [], out_dir / f"{stem}.yaml")
            all_log_lines.extend(log_lines)
        except Exception as e:
            print(f"[ERROR] processing {stem} failed: {e}")
            all_log_lines.append(f"ERROR processing {stem}: {e}")
    (LOG_DIR / "pipeline.log").write_text("\n".join(all_log_lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="M1 batch to output/<stem> with progress printing")
    parser.add_argument("--no-cache", action="store_true", help="do not use .dolphin_cache/markdown as fallback")
    parser.add_argument("--no-dolphin", action="store_true", help="do not auto-run Dolphin or synthesize md when missing")
    parser.add_argument("--persist-md", action="store_true", help="when using cache/generated md, also save to data/<stem>.md")
    parser.add_argument("--only", type=str, default=None, help="process only one stem, e.g. --only mcp9700")
    parser.add_argument("--dolphin-timeout", type=int, default=0, help="seconds to wait per Dolphin run (0=no timeout)")
    parser.add_argument("--dolphin-batch", type=int, default=MAX_BATCH, help="max_batch_size for Dolphin inference")
    args = parser.parse_args()
    use_cache = not args.no_cache
    print("[INFO] M1 batch -> output/<stem>/{stem.json, stem.yaml, source.md?}; logs/pipeline.log")
    print(f"[INFO] use_cache={use_cache}, auto_generate_md={not args.no_dolphin}, persist_md={args.persist_md}")
    if args.only:
        print(f"[INFO] only={args.only}")
    if not args.no_dolphin:
        print(f"[INFO] dolphin_timeout={args.dolphin_timeout}s, dolphin_batch={args.dolphin_batch}")
    run_batch(
        use_dolphin_cache=use_cache,
        persist_md=args.persist_md,
        use_dolphin_when_missing=not args.no_dolphin,
        dolphin_timeout=args.dolphin_timeout,
        dolphin_batch=args.dolphin_batch,
        only=args.only,
    )


if __name__ == "__main__":
    main()
