# -*- coding: utf-8 -*-
"""
通过主字典 master_dictionary.csv 来进行同义词字典扩充（IoT 版本，英文收敛、溯源可追）。

输入
----
master_dictionary.csv : 两种格式其一：
  A) id,parent_id,content,category,notes
  B) Id,Search_Category_Name               （平面一级类，category 固定写 'group'）

output/**/*.md        : Markdown 语料（递归扫描）
device_index.csv      : (可选) device_id,device_name,file_glob
param_lexicon.yaml    : (可选) 参数家族配置，用于扩展启发式触发词

输出
----
dict_v1.jsonl         : 主字典各条目的同义词与证据（来源、位置）
dict_tree.csv         : 树形视图（按主字典顺序编号；同义词为 13.01 格式）
occurrences.jsonl     : 每一次命中的溯源记录（设备/文件/行/列/章节）
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

# 可选依赖（当前未启用的占位）
try:
    import requests  # type: ignore
except Exception:
    requests = None

try:
    from sentence_transformers import SentenceTransformer, util  # type: ignore
except Exception:
    SentenceTransformer = None
    util = None


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Concept:
    concept_id: str
    parent_id: Optional[str]
    content: str
    category: str
    notes: str
    children: List[str] = field(default_factory=list)
    seq: int = 0  # 保序用


@dataclass
class SynonymEntry:
    term: str
    sources: Set[str] = field(default_factory=set)
    evidence: List[Dict[str, object]] = field(default_factory=list)

    def to_json(self) -> Dict[str, object]:
        return {"term": self.term, "source": sorted(self.sources), "evidence": self.evidence}


# ---------------------------------------------------------------------------
# 工具函数（清洗、归一化、映射）
# ---------------------------------------------------------------------------

LATEX_REPLACEMENTS = {
    r"\\mu": "µ",
    r"\\Omega": "Ω",
    r"\\degC": "°C",
    r"\\degreeC": "°C",
    r"\\deg": "°",
    r"\\alpha": "α",
    r"\\beta": "β",
    r"\\gamma": "γ",
    r"\\pm": "±",
}

def demath(s: str) -> str:
    """
    去除行内 TeX/LaTeX、常见命令转 Unicode、去上下标格式，合并空白。
    例如：'$V_{\\text{i}}$' -> 'Vi'
    """
    if not isinstance(s, str):
        return ""
    t = s
    # 去 $...$
    t = re.sub(r"\$([^$]*)\$", r"\1", t)
    # 命令替换
    for pat, rep in LATEX_REPLACEMENTS.items():
        t = re.sub(pat, rep, t)
    # \text{...} 等展开
    t = re.sub(r"\\(?:text|mathrm|operatorname)\s*\{([^}]*)\}", r"\1", t)
    # 上/下标去格式
    t = re.sub(r"[_^]\s*\{([^}]*)\}", r"\1", t)
    t = re.sub(r"[_^]\s*([A-Za-z0-9]+)", r"\1", t)
    # 残余命令砍掉
    t = re.sub(r"\\[A-Za-z]+", "", t)
    # 清理大括号
    t = t.replace("{", "").replace("}", "")
    # 单位紧凑
    t = re.sub(r"\b([µu])\s*([AVWHz])\b", r"\1\2", t)
    t = re.sub(r"\b(m|k|G)\s*([AVWHzbps])\b", r"\1\2", t)
    # 合并空白
    t = re.sub(r"\s+", " ", t).strip()
    return t


def normalize_key(term: str) -> str:
    t = unicodedata.normalize("NFKC", demath(term))
    t = re.sub(r"\s+", "", t)
    return t.lower()


def strip_term(term: str) -> str:
    t = demath(term)
    t = unicodedata.normalize("NFKC", t)
    t = t.strip(" []()（）「」『』【】“”\"'`･·・-‐-‒–—―、。,.;:：/\\")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _jp_collapse(s: str) -> str:
    """日文长名收敛：去中点、全角化、去空白，用作 key。"""
    t = unicodedata.normalize("NFKC", s)
    t = t.replace("・", "").replace("･", "")
    t = re.sub(r"\s+", "", t)
    return t


# ---------------------------------------------------------------------------
# 映射词典（可扩展）
# ---------------------------------------------------------------------------

JP_CHAR_RE = re.compile(r"[\u3040-\u30FF\u31F0-\u31FF\u4E00-\u9FFF]")

# 日->英（参数/常见词）
JP_TO_EN_MAP: Dict[str, str] = {
    unicodedata.normalize("NFKC", k): v
    for k, v in {
        "電源電圧": "Power Supply Voltage",
        "供給電圧": "Supply Voltage",
        "入力電圧": "Input Voltage",
        "出力電圧": "Output Voltage",
        "電源電流": "Power Supply Current",
        "動作電流": "Operating Current",
        "消費電流": "Consumption Current",
        "帯域幅": "Bandwidth",
        "ノイズ": "Noise",
        "感度": "Sensitivity",
        "線形性": "Linearity",
        "精度": "Accuracy",
        "分解能": "Resolution",
        "周波数": "Frequency",
        "クロック": "Clock",
        "温度": "Temperature",
        "動作温度": "Operating Temperature",
        "保存温度": "Storage Temperature",
        "湿度": "Humidity",
        "信頼性": "Reliability",
        "耐久性": "Durability",
        "防塵": "Dust Protection",
        "防水": "Waterproofing",
        "ケース": "Enclosure",
        "外形": "Form Factor",
        "寸法": "Dimensions",
        "重量": "Weight",
        "用途": "Application",
        "機能": "Function",
        "更新": "Update",
        "アップデート": "Update",
        "ライブラリ": "Library",
        "アクチュエータ": "Actuator",
        "品番": "Part Number",
        "型番": "Model Number",
        "製品番号": "Product Number",
        "認証": "Certification",
        "温度範囲": "Temperature Range",
        "温度入力範囲": "Temperature Input Range",
        "光センサー": "Light Sensor",
        "気圧センサー": "Barometric Pressure Sensor",
        "供給電流": "Supply Current",
        "消費電力": "Power Consumption",
    }.items()
}

# 日文长名 → 英文缩写/英文名（例如 SPI 的全称）
JP_LONGFORM_TO_EN = {
    _jp_collapse("シリアル・ペリフェラル・インターフェース"): "SPI",
    _jp_collapse("ユニバーサルシリアルバス"): "USB",
    # 读音补充（可选）：
    _jp_collapse("アイツーシー"): "I2C",
    _jp_collapse("ユーアールエーティー"): "UART",
}

def collapse_jp_with_ascii_fallback(jp_term: str, ascii_anchor: str) -> Optional[str]:
    """
    当 candidate 是日文且未映射时，利用当前触发 token（ascii_anchor）做英文收敛：
      1) 命中 JP_LONGFORM_TO_EN -> 返回其英文
      2) 否则如果 ascii_anchor 是短缩写（<=5 且字母/数字/+-/斜杠），返回 anchor.upper()
    """
    if not jp_term or not ascii_anchor:
        return None
    key = _jp_collapse(jp_term)
    if key in JP_LONGFORM_TO_EN:
        return JP_LONGFORM_TO_EN[key]
    anchor = unicodedata.normalize("NFKC", ascii_anchor).strip()
    if 1 <= len(anchor) <= 5 and re.fullmatch(r"[A-Za-z0-9\-/+]+", anchor):
        return anchor.upper()
    return None


# ---------------------------------------------------------------------------
# 主字典 / 设备索引 / 参数家族
# ---------------------------------------------------------------------------

def load_master(master_path: str) -> Dict[str, Concept]:
    if not os.path.isfile(master_path):
        raise FileNotFoundError(f"master dictionary not found: {master_path}")

    with open(master_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        concepts: Dict[str, Concept] = {}
        row_idx = 0

        if set(fieldnames) >= {"id", "parent_id", "content", "category", "notes"}:
            for row in reader:
                cid = row["id"].strip()
                if not cid:
                    continue
                if cid in concepts:
                    raise ValueError(f"duplicate concept id detected: {cid}")
                parent_id = row["parent_id"].strip() or None
                row_idx += 1
                concepts[cid] = Concept(
                    concept_id=cid,
                    parent_id=parent_id,
                    content=row["content"].strip(),
                    category=row["category"].strip(),
                    notes=row.get("notes", "").strip(),
                    seq=row_idx,
                )
        elif set(fieldnames) >= {"Id", "Search_Category_Name"}:
            for row in reader:
                cid = row["Id"].strip()
                name = row["Search_Category_Name"].strip()
                if not cid or not name:
                    continue
                if cid in concepts:
                    raise ValueError(f"duplicate concept id detected: {cid}")
                row_idx += 1
                concepts[cid] = Concept(
                    concept_id=cid,
                    parent_id=None,
                    content=name,
                    category="group",
                    notes="",
                    seq=row_idx,
                )
        else:
            raise ValueError(
                "master dictionary must include either "
                "(id,parent_id,content,category,notes) or (Id,Search_Category_Name)"
            )

        # 建立孩子链接
        for c in concepts.values():
            if c.parent_id and c.parent_id in concepts:
                concepts[c.parent_id].children.append(c.concept_id)

        return concepts


def ordered_concepts(concepts: Dict[str, Concept]) -> List[Concept]:
    """按 DFS 且保持 seq 的顺序输出。"""
    roots = [c for c in concepts.values() if not c.parent_id or c.parent_id not in concepts]
    roots.sort(key=lambda c: c.seq)
    out: List[Concept] = []
    for root in roots:
        stack = deque([(root, 0)])
        while stack:
            node, _ = stack.pop()
            out.append(node)
            children = [concepts[cid] for cid in node.children]
            children.sort(key=lambda c: c.seq, reverse=True)
            for child in children:
                stack.append((child, 0))
    return out


@dataclass
class DeviceMapping:
    device_id: str
    device_name: str
    pattern: str


def load_device_index(path: Optional[str]) -> List[DeviceMapping]:
    if not path:
        return []
    if not os.path.isfile(path):
        raise FileNotFoundError(f"device index not found: {path}")
    res: List[DeviceMapping] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"device_id", "device_name", "file_glob"}
        if not required.issubset(reader.fieldnames or set()):
            raise ValueError(f"device index must include columns: {sorted(required)}")
        for row in reader:
            res.append(
                DeviceMapping(
                    device_id=row["device_id"].strip(),
                    device_name=row["device_name"].strip(),
                    pattern=row["file_glob"].strip(),
                )
            )
    return res


def resolve_device(file_rel: str, mappings: List[DeviceMapping]) -> Tuple[Optional[str], Optional[str]]:
    for m in mappings:
        if fnmatch.fnmatch(file_rel, m.pattern):
            return m.device_id, m.device_name
    return None, None


def load_param_lexicon(path: Optional[str]) -> Dict[str, Dict[str, object]]:
    if not path:
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required for --param-conf but is not installed.")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"parameter lexicon not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    families = data.get("parameter_families", {}) if isinstance(data, dict) else {}
    sanitized: Dict[str, Dict[str, object]] = {}
    for name, cfg in families.items():
        if not isinstance(cfg, dict):
            continue
        category = cfg.get("category")
        if not category:
            continue
        sanitized[name] = {"category": str(category).strip()}
        for key in ("triggers", "jp", "en", "abbrev", "units"):
            values = cfg.get(key, [])
            if isinstance(values, list):
                sanitized[name][key] = [str(v).strip() for v in values if str(v).strip()]
            else:
                sanitized[name][key] = []
    return sanitized


# ---------------------------------------------------------------------------
# 同义词存储
# ---------------------------------------------------------------------------

class SynonymStore:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, SynonymEntry]] = defaultdict(dict)

    def add(self, concept_id: str, term: str, source: str,
            evidence: Optional[Dict[str, object]] = None) -> bool:
        term_clean = strip_term(term)
        if not term_clean:
            return False
        key = normalize_key(term_clean)
        entry = self._store[concept_id].get(key)
        if entry is None:
            entry = SynonymEntry(term=term_clean)
            self._store[concept_id][key] = entry
        entry.sources.add(source)
        if evidence:
            entry.evidence.append(evidence)
        return True

    def get_terms(self, concept_id: str) -> List[SynonymEntry]:
        return sorted(self._store.get(concept_id, {}).values(), key=lambda e: e.term.lower())


# ---------------------------------------------------------------------------
# 启发式词表（仅作为初始触发/同义词）
# ---------------------------------------------------------------------------

BASE_HEURISTICS: Dict[str, List[str]] = {
    "Device_Metadata": [
        "Device Name", "Model Number", "Part Number", "Product Name",
        "Datasheet", "Revision", "Firmware Version",
    ],
    "Device_Function": ["Application", "Function", "Use Case", "Feature", "Target Use"],
    "Power_System": [
        "Power Supply Voltage", "Supply Voltage", "Input Voltage", "Output Voltage",
        "Power Supply Current", "Operating Current", "Consumption Current",
        "Power Consumption", "Supply Current", "Vcc", "VDD", "VIN", "VOUT", "ICC", "IIN", "IOUT",
    ],
    "Electrical_Performance": ["Accuracy", "Bandwidth", "Noise", "Sensitivity", "Linearity", "Resolution", "Offset", "Gain"],
    "RF_Wireless": ["Wi-Fi", "Bluetooth", "BLE", "LoRa", "LoRaWAN", "ZigBee", "Sub-GHz", "RF", "Radio", "ISM Band", "2.4 GHz", "5 GHz", "Antenna", "RSSI"],
    "Wired_Interface": ["SPI", "I2C", "UART", "RS-485", "RS-232", "CAN", "Modbus", "USB", "EtherCAT", "GPIO", "PWM"],
    "Network_Connectivity": ["Ethernet", "IP Address", "TCP/IP", "UDP", "MAC Address", "Network Protocol", "MQTT", "HTTP", "CoAP"],
    "Timing_Clock": ["Clock", "Oscillator", "PLL", "Frequency", "Jitter", "ppm"],
    "Sensors": ["Temperature Sensor", "Humidity Sensor", "Accelerometer", "Gyroscope", "Magnetometer", "Pressure Sensor", "Sensing Range"],
    "Actuators": ["Actuator", "Motor", "Servo", "Driver", "Relay", "Valve"],
    "Firmware_Software": ["Firmware", "Software", "SDK", "API", "Library", "Bootloader", "Update"],
    "Storage_Memory": ["Flash", "EEPROM", "SD Card", "RAM", "ROM", "Memory", "Storage", "Capacity"],
    "Security_Privacy": ["Encryption", "TLS", "SSL", "Authentication", "Secure Boot", "Key Management", "Security"],
    "Environmental_Reliability": ["Operating Temperature", "Storage Temperature", "Humidity", "Ingress Protection", "IP Rating", "Reliability", "ESD", "EMC"],
    "Mechanical_Enclosure": ["Dimensions", "Weight", "Enclosure", "Housing", "Mounting", "Form Factor"],
    "Certification_Standard": ["CE", "FCC", "RoHS", "UL", "IEC", "JIS", "ISO", "Certification", "Compliance"],
    "Testing_Quality": ["Testing", "Quality", "Inspection", "QA", "Validation"],
    "Diagnostics_Maintenance": ["Diagnostic", "Self-Test", "Maintenance", "Monitoring", "Status", "Health Check", "Log"],
}

# 只用于搜索触发，绝不进入同义词输出
BASE_SEARCH_ONLY: Dict[str, List[str]] = {
    "Device_Metadata": ["型番", "品番", "製品番号"],
    "Device_Function": ["用途", "機能"],
    "Power_System": ["電源電圧", "供給電圧", "入力電圧", "出力電圧", "電源電流", "動作電流", "消費電流"],
    "Electrical_Performance": ["精度", "帯域幅", "ノイズ", "感度", "線形性", "分解能"],
    "Environmental_Reliability": ["動作温度", "保存温度", "湿度"],
    "Mechanical_Enclosure": ["寸法", "重量", "ケース", "外形"],
    "Firmware_Software": ["更新", "アップデート", "ライブラリ"],
    "Actuators": ["アクチュエータ"],
    "Security_Privacy": ["認証", "鍵"],
    "Testing_Quality": ["試験", "測定"],
    "Diagnostics_Maintenance": ["監視"],
    "Storage_Memory": ["容量"],
    "Sensors": ["光センサー", "気圧センサー", "感度"],
    "Timing_Clock": ["クロック", "周波数"],
}

GLOBAL_BLACKLIST = {"センサ", "センサー", "sensor", "module", "device", "power", "current", "voltage"}

PARAM_WHITELIST_LOWER = {"voltage", "current", "temperature", "temp", "v", "i", "a", "°c", "c", "bandwidth"}


def canonical_variants(content: str) -> Set[str]:
    variants = {content}
    nk = unicodedata.normalize("NFKC", content)
    variants.add(nk)
    variants.add(nk.lower())
    variants.add(re.sub(r"\s+", "", nk))
    variants.add(re.sub(r"[／/]", "/", nk))
    return {v for v in variants if v}


def find_patterns(line: str, token: str) -> List[str]:
    """从局部窗口提取 A(B)、B(A)、A/B、B/A、aka: X 等别名候选。"""
    results: List[str] = []
    pattern_after = re.compile(rf"{re.escape(token)}\s*[\(（]\s*([^)）]{{1,40}})\s*[\)）]", re.IGNORECASE)
    pattern_before = re.compile(rf"([^\(（\s]{{1,40}})\s*[\(（]\s*{re.escape(token)}\s*[\)）]", re.IGNORECASE)
    pattern_slash = re.compile(rf"{re.escape(token)}\s*/\s*([^\s、，,;；]{{1,40}})", re.IGNORECASE)
    pattern_slash_rev = re.compile(rf"([^\s、，,;；]{{1,40}})\s*/\s*{re.escape(token)}", re.IGNORECASE)
    pattern_aka = re.compile(rf"(aka|別名|略称|also known as)\s*[:：]?\s*([^\s、，,;；]{{1,40}})", re.IGNORECASE)

    for pat in (pattern_after, pattern_before, pattern_slash, pattern_slash_rev):
        for m in pat.finditer(line):
            results.append(m.group(1))
    for m in pattern_aka.finditer(line):
        results.append(m.group(2))
    return results


def valid_candidate(candidate: str, category: str) -> bool:
    cand = strip_term(candidate)
    if not cand or len(cand) < 2 or len(cand) > 60:
        return False
    cand_lower = unicodedata.normalize("NFKC", cand).lower()
    if any(sym in cand for sym in ("<", ">", "=", "|", "\"")):
        return False
    if re.search(r"(?:rowspan|colspan|table)", cand_lower):
        return False
    if cand_lower in GLOBAL_BLACKLIST and category != "parameter":
        return False
    if category == "parameter":
        if cand_lower in GLOBAL_BLACKLIST and cand_lower not in PARAM_WHITELIST_LOWER:
            return False
    return True


def to_storage_term(term: str) -> Optional[str]:
    """
    统一输出到英文空间：
      - 英文/ASCII：直接标准化返回
      - 日文：若命中 JP_LONGFORM_TO_EN 或 JP_TO_EN_MAP -> 英文；否则 None（不直接输出日文）
    """
    cleaned = strip_term(term)
    if not cleaned:
        return None
    normalized = unicodedata.normalize("NFKC", cleaned)

    if JP_CHAR_RE.search(normalized):
        key = _jp_collapse(normalized)
        if key in JP_LONGFORM_TO_EN:
            return JP_LONGFORM_TO_EN[key]
        mapped = JP_TO_EN_MAP.get(normalized)
        if mapped:
            return mapped
        return None  # 未映射的日文默认不输出
    return normalized


def relpath(path: str, root: str) -> str:
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return path


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="IoT master-dictionary driven synonym expander.")
    parser.add_argument("--master", default="master_dictionary.csv")
    parser.add_argument("--root", default="output")
    parser.add_argument("--out-jsonl", default="dict_v1.jsonl")
    parser.add_argument("--out-tree", default="dict_tree.csv")
    parser.add_argument("--occ", default="occurrences.jsonl")
    parser.add_argument("--window", type=int, default=96)
    parser.add_argument("--langs", default="ja,en")
    parser.add_argument("--cache", default=".wiki_cache.json")
    parser.add_argument("--th", type=float, default=0.78)
    parser.add_argument("--device-index")
    parser.add_argument("--param-conf")
    parser.add_argument("--no-wiki", action="store_true")
    parser.add_argument("--no-embed", action="store_true")
    args = parser.parse_args()

    # 读主字典
    try:
        concepts = load_master(args.master)
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    ordered = ordered_concepts(concepts)

    # 语料存在性
    if not os.path.isdir(args.root):
        print(f"ERROR: corpus root not found: {args.root}")
        sys.exit(1)

    # 可选：设备索引
    try:
        device_mappings = load_device_index(args.device_index)
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    # 可选：参数家族
    try:
        param_families = load_param_lexicon(args.param_conf)
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    if not args.no_wiki:
        print("WARN: wiki integration not implemented in this build; skipping wiki candidates.")
    if not args.no_embed:
        print("WARN: embedding filter not implemented in this build; skipping semantic filtering.")

    synonym_store = SynonymStore()
    search_terms: Dict[str, Set[str]] = defaultdict(set)

    # 1) 启发式（进入同义词+搜索）
    for concept in ordered:
        base_terms = BASE_HEURISTICS.get(concept.concept_id) or BASE_HEURISTICS.get(concept.content) or []
        for term in base_terms:
            storage = to_storage_term(term)
            if not storage:
                continue
            if synonym_store.add(concept.concept_id, storage, "heuristic"):
                search_terms[concept.concept_id].add(storage)

        # 2) 只用于搜索，不进入同义词
        search_only = BASE_SEARCH_ONLY.get(concept.concept_id) or BASE_SEARCH_ONLY.get(concept.content) or []
        for term in search_only:
            search_terms[concept.concept_id].add(term)
            storage = to_storage_term(term)
            if storage:
                search_terms[concept.concept_id].add(storage)

        # 3) 参数家族（若提供）
        if param_families:
            for _fam_name, cfg in param_families.items():
                target_category = str(cfg.get("category", "")).strip()
                if target_category not in (concept.concept_id, concept.content):
                    continue
                aggregate: Set[str] = set()
                for key in ("jp", "en", "abbrev", "units", "triggers"):
                    for term in cfg.get(key, []):
                        if term:
                            aggregate.add(str(term).strip())
                for term in sorted(aggregate):
                    search_terms[concept.concept_id].add(term)
                    storage = to_storage_term(term)
                    if storage and synonym_store.add(concept.concept_id, storage, "heuristic"):
                        search_terms[concept.concept_id].add(storage)

    # 4) 为每个概念加入 canonical 形态，保证标题/下划线/小写等都能触发
    for concept in ordered:
        for variant in canonical_variants(concept.content):
            search_terms[concept.concept_id].add(variant)
        display_variant = concept.content.replace("_", " ")
        search_terms[concept.concept_id].add(display_variant)
        search_terms[concept.concept_id].add(display_variant.lower())
        for entry in synonym_store.get_terms(concept.concept_id):
            search_terms[concept.concept_id].add(entry.term)

    # 5) 扫描 Markdown
    occurrences: List[Dict[str, object]] = []

    md_files = [
        os.path.join(root, file)
        for root, _dirs, files in os.walk(args.root)
        for file in files
        if file.lower().endswith(".md")
    ]
    md_files.sort()

    heading_pattern = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)")
    fence_pattern = re.compile(r"^\s*```")

    for file_path in md_files:
        rel = relpath(file_path, args.root)
        device_id, device_name = resolve_device(rel, device_mappings)

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        section = ""
        in_code = False

        for lineno, raw_line in enumerate(lines, start=1):
            line = raw_line.rstrip("\n")
            if fence_pattern.match(line):
                in_code = not in_code
                continue
            if in_code:
                continue

            m = heading_pattern.match(line)
            if m:
                section = strip_term(m.group(2))
                continue

            # 先数学清洗
            line = demath(line)
            line_lower = line.lower()

            for concept in ordered:
                tokens_snapshot = list(search_terms[concept.concept_id])
                for token in tokens_snapshot:
                    token_clean = token.strip()
                    if not token_clean:
                        continue
                    token_lower = unicodedata.normalize("NFKC", token_clean).lower()

                    pointer = 0
                    while True:
                        idx = line_lower.find(token_lower, pointer)
                        if idx == -1:
                            break
                        prev_char = line[idx - 1] if idx > 0 else " "
                        next_index = idx + len(token_clean)
                        next_char = line[next_index] if next_index < len(line) else " "
                        if prev_char.isalnum() or prev_char == "_" or next_char.isalnum() or next_char == "_":
                            pointer = idx + max(1, len(token_clean))
                            continue

                        match_text = line[idx: idx + len(token_clean)]
                        col_start, col_end = idx, idx + len(match_text)

                        # 记录一次命中
                        occ_record = {
                            "device_id": device_id,
                            "device_name": device_name,
                            "concept_id": concept.concept_id,
                            "match_term": match_text,
                            "span": {"file": rel, "line": lineno, "col_start": col_start, "col_end": col_end, "section": section},
                            "context": line.strip(),
                            "normalized_to": concept.content,
                            "category": concept.category,
                        }
                        occurrences.append(occ_record)

                        evidence = {
                            "file": rel,
                            "line": lineno,
                            "col_start": col_start,
                            "col_end": col_end,
                            "section": section,
                        }

                        # 把本次命中的文本归一化到英文空间（若可能）
                        storage_match = to_storage_term(match_text)
                        if storage_match and normalize_key(storage_match) != normalize_key(concept.content):
                            if synonym_store.add(concept.concept_id, storage_match, "md", evidence):
                                search_terms[concept.concept_id].add(storage_match)
                        # 原词加入触发集合（强化后续匹配）
                        search_terms[concept.concept_id].add(match_text)

                        # 模式抽取（括号/斜杠/aka），对日文 candidate 做英文收敛
                        window_start = max(0, idx - args.window)
                        window_end = min(len(line), idx + len(match_text) + args.window)
                        window_text = line[window_start:window_end]
                        for candidate in find_patterns(window_text, match_text):
                            candidate_clean = strip_term(candidate)
                            if not candidate_clean:
                                continue
                            if not valid_candidate(candidate_clean, concept.category):
                                continue
                            if normalize_key(candidate_clean) == normalize_key(concept.content):
                                continue

                            storage_candidate = to_storage_term(candidate_clean)

                            # 未映射日文 -> 尝试用当前 ASCII token 收敛
                            if storage_candidate is None and JP_CHAR_RE.search(candidate_clean):
                                ascii_back = collapse_jp_with_ascii_fallback(candidate_clean, match_text)
                                if ascii_back:
                                    storage_candidate = to_storage_term(ascii_back)

                            if storage_candidate and normalize_key(storage_candidate) != normalize_key(concept.content):
                                if synonym_store.add(concept.concept_id, storage_candidate, "md", evidence):
                                    search_terms[concept.concept_id].add(storage_candidate)

                            # candidate 自身加入触发集合（不一定入库）
                            search_terms[concept.concept_id].add(candidate_clean)

                        pointer = idx + len(token_clean)

    # 写 JSONL（同义词）
    with open(args.out_jsonl, "w", encoding="utf-8") as f_json:
        for concept in ordered:
            synonym_entries = synonym_store.get_terms(concept.concept_id)
            payload = {
                "id": concept.concept_id,
                "content": concept.content,
                "category": concept.category,
                "synonyms": [entry.to_json() for entry in synonym_entries],
                "frozen": True,
            }
            f_json.write(json.dumps(payload, ensure_ascii=False) + "\n")

    # 写树 CSV（按主字典顺序编号；同义词 13.01 形式；同义词行不重复类别）
    with open(args.out_tree, "w", encoding="utf-8", newline="") as f_tree:
        writer = csv.writer(f_tree)
        writer.writerow(["index", "term", "category"])

        def depth_of(c: Concept) -> int:
            d = 0; p = c.parent_id
            while p and p in concepts:
                d += 1; p = concepts[p].parent_id
            return d

        # 顶层（无 parent 或 parent 不存在），按 seq 排
        top_level = [c for c in ordered if not c.parent_id or c.parent_id not in concepts]
        top_level_sorted = sorted(top_level, key=lambda c: c.seq)
        top_index_map = {c.concept_id: i + 1 for i, c in enumerate(top_level_sorted)}
        sub_counters: Dict[str, int] = defaultdict(int)

        for concept in ordered:
            d = depth_of(concept)
            indent = "  " * d
            display = concept.content.replace("_", " ")

            # 找所属顶层
            top_parent = concept
            while top_parent.parent_id and top_parent.parent_id in concepts:
                top_parent = concepts[top_parent.parent_id]
            top_id = top_parent.concept_id

            if concept.concept_id in top_index_map:
                idx = str(top_index_map[concept.concept_id])
                sub_counters[concept.concept_id] = 0
            elif top_id in top_index_map and d >= 1:
                idx = f"{top_index_map[top_id]}.00"
            else:
                idx = ""

            # 概念行
            writer.writerow([idx, f"{indent}{display}", concept.category])

            # 同义词行（只输出 term，不重复类别）
            if top_id in top_index_map:
                base_no = top_index_map[top_id]
                for entry in synonym_store.get_terms(concept.concept_id):
                    sub_counters[top_id] += 1
                    sub_idx = f"{base_no}.{sub_counters[top_id]:02d}"
                    writer.writerow([sub_idx, f"{indent}  {entry.term}", ""])

    # 写溯源
    with open(args.occ, "w", encoding="utf-8") as f_occ:
        for record in occurrences:
            f_occ.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"done {args.out_jsonl} {args.out_tree} {args.occ}")
    print("entries=", len(ordered), "with_synonyms=",
          sum(1 for c in ordered if len(synonym_store.get_terms(c.concept_id)) > 0))


if __name__ == "__main__":
    main()
