# rules.py —— 关键词/正则抽取逻辑

import re
from typing import List, Dict, Any

# 多语言同义词词典
SYNONYMS = {
    "power": ["VDD", "VCC", "供給電圧", "電源電圧", "供电电压", "Operating voltage"],
    "sensitivity": ["10 mV/°C", "10mV/°C", "温度係数", "温度勾配"],
    "spi_mode": ["SPI Mode 3", "CPOL=1, CPHA=1", "SPI モード"],
    "range": ["範囲", "Range", "量程", "0–14 pH", "±200 A", "±5 g"],
}

# 常见字段正则模式（可逐步扩展）
PATTERNS = {
    "electrical.vdd_range": r"(?:2\.7\s*V\s*[–\-~]\s*10\s*V|2\.3\s*V\s*[–\-~]\s*5\.5\s*V|4\.5\s*V\s*[–\-~]\s*5\.5\s*V)",
    "sensitivity": r"(?:10\s*mV\/°C)",
    "interface.spi.mode": r"(?:SPI\s*Mode\s*3|CPOL\s*=\s*1\s*,?\s*CPHA\s*=\s*1)",
    "sampling.rate": r"(\b[12]0?48\s*SPS\b)",
    "sensing.min_particle": r"(?:0\.5\s*[µu]m|0\.5um)",
    "sensing.ph_range": r"(?:0\s*[–\-~]\s*14\s*pH)",
}

def build_queries(schema_keys: List[str]) -> List[str]:
    """根据 schema key 构造查询词列表"""
    queries = []
    for k in schema_keys:
        queries += SYNONYMS.get(k, [k])
    # 去重保持顺序
    seen, out = set(), []
    for q in queries:
        if q not in seen:
            out.append(q)
            seen.add(q)
    return out

def extract_spec(blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    
    text = "\n".join(b["content"] for b in blocks if b["type"] != "table")
    spec = {"_evidence": []}

    def accept(field, pattern):
        m = re.search(pattern, text, flags=re.I)
        if not m:
            return
        val = m.group(0)
        spec[field] = val
        ev = next((b for b in blocks if val in (b["content"] or "")), None)
        spec["_evidence"].append({
            "field": field,
            "value": val,
            "page": ev["page"] if ev else None,
            "bbox": ev["bbox"] if ev else None,
            "snippet": (ev["content"][:200] if ev else "")
        })

    for f, pat in PATTERNS.items():
        accept(f, pat)

    return spec
