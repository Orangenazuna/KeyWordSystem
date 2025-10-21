import json, glob, os, sys

# ---- 1. 兼容 Document 的导入方式 ---------------------------------
try:
    from langchain_core.documents import Document  # 新版 (>=0.3)
except ImportError:
    try:
        from langchain.schema import Document      # 中期版
    except ImportError:
        from langchain.docstore.document import Document  # 旧版

# ---- 2. 兼容 TextSplitter 的导入方式 --------------------------------
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # 新
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter   # 旧

# ---- 3. 向量库 Chroma ------------------------------------------------
from langchain_community.vectorstores import Chroma

# ---- 4. Embedding: langchain-huggingface 优先 ------------------------
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except ImportError:
        from langchain.embeddings import HuggingFaceEmbeddings  # 最旧兜底

PERSIST_DIR = "./db/chroma_store"

# 关键修改：你现在的文件实际在 ./output 下面
DATA_DIR = "./output"


def normalize_items_from_any_shape(raw_loaded, filename_hint):
    """
    把各种形状的JSON转换成统一的:
    [
      {"file": "...", "page": <int>, "text": "..."},
      ...
    ]
    """
    norm = []

    # 情况1: 已经是list，而且元素是dict，里面有text/page等字段
    if isinstance(raw_loaded, list):
        for idx, entry in enumerate(raw_loaded):
            # entry 可能是 dict，也可能是 string
            if isinstance(entry, dict):
                # 尝试取 file / page / text
                file_val = entry.get("file", filename_hint)
                page_val = entry.get("page", idx + 1)
                text_val = entry.get("text", "") or ""
                text_val = text_val.strip()

                if text_val:
                    norm.append({
                        "file": file_val,
                        "page": page_val,
                        "text": text_val,
                    })
            elif isinstance(entry, str):
                # 如果只是 ["textpage1", "textpage2", ...] 这种
                text_val = entry.strip()
                if text_val:
                    norm.append({
                        "file": filename_hint,
                        "page": idx + 1,
                        "text": text_val,
                    })
            else:
                # 其他类型（比如数字、None）无视
                pass

        return norm

    # 情况2: 是一个 dict，比如:
    # {
    #   "file": "xxx.pdf",
    #   "pages": [
    #       {"page":1,"text":"..."},
    #       {"page":2,"text":"..."}
    #   ]
    # }
    if isinstance(raw_loaded, dict):
        base_file = raw_loaded.get("file", filename_hint)
        if "pages" in raw_loaded and isinstance(raw_loaded["pages"], list):
            for idx, pg in enumerate(raw_loaded["pages"]):
                if isinstance(pg, dict):
                    page_val = pg.get("page", idx + 1)
                    text_val = pg.get("text", "") or ""
                    text_val = text_val.strip()
                    if text_val:
                        norm.append({
                            "file": base_file,
                            "page": page_val,
                            "text": text_val,
                        })
                elif isinstance(pg, str):
                    text_val = pg.strip()
                    if text_val:
                        norm.append({
                            "file": base_file,
                            "page": idx + 1,
                            "text": text_val,
                        })
        else:
            # dict 但没有 "pages"，也可能有 "text" 自己一段
            text_val = (raw_loaded.get("text") or "").strip()
            if text_val:
                norm.append({
                    "file": base_file,
                    "page": raw_loaded.get("page", 1),
                    "text": text_val,
                })
        return norm

    # 兜底: raw_loaded 不是 list 也不是 dict
    # 我们直接放弃它
    return norm


def load_cleaned_docs():
    items_all = []
    paths = glob.glob(os.path.join(DATA_DIR, "*.json"))
    print(f"[DEBUG] 找到 {len(paths)} 个JSON文件于 {DATA_DIR}")

    for path in paths:
        print(f"[DEBUG] 读取: {path}")
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        filename_hint = os.path.basename(path)
        norm_items = normalize_items_from_any_shape(raw, filename_hint)

        print(f"[DEBUG] {path} 解析后得到 {len(norm_items)} 段")
        items_all.extend(norm_items)

    print(f"[DEBUG] 合计段落数: {len(items_all)}")
    return items_all


def build_documents(items):
    docs = []
    for obj in items:
        docs.append(
            Document(
                page_content=obj["text"],
                metadata={
                    "file": obj["file"],
                    "page": obj["page"],
                }
            )
        )
    print(f"[DEBUG] LangChain Document 数量: {len(docs)}")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"[DEBUG] 切块后 chunk 数量: {len(chunks)}")
    return chunks


def build_vectorstore(chunks):
    if not chunks:
        print("[ERROR] 没有任何chunk，无法建立向量库。请检查 JSON 格式是否含文本。")
        sys.exit(1)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    print("[DEBUG] Embedding 模型加载完成")

    vs = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR
    )
    vs.persist()
    print(f"[DEBUG] 向量库已写入 {PERSIST_DIR}")
    return vs


if __name__ == "__main__":
    items = load_cleaned_docs()
    docs = build_documents(items)
    chunks = split_documents(docs)
    build_vectorstore(chunks)
    print("✅ ingest 完成")
