# 🧠 IoT-RAG: Multi-Modal Knowledge Extraction and Intelligent Agent System

本研究项目分为两个阶段，分别对应两篇论文的技术主线：
1. **Part I — IoT-RAG 基础系统：多模态数据的RAG智能问答与知识检索系统**
2. **Part II — IoT-RAG++ 改进系统：混合检索与多轮对话增强的智能Agent系统**

---

## 🚀 Part I：IoT-RAG 基础系统 — 多模态数据RAG智能问答与知识检索系统

### 🎯 研究目标
构建一个支持多格式（PDF、DOCX、TXT、JPG等）IoT文档解析与知识检索的 **RAG（Retrieval-Augmented Generation）** 系统，通过LLM结合数据库实现设备文档、传感器参数的智能问答与知识检索。

### 🧩 核心技术结构

| 模块 | 使用技术 | 功能描述 |
|------|-----------|-----------|
| **1. 数据解析层** | LangChain + OCR + PyMuPDF + python-docx | 自动识别与提取PDF、Word、图片等IoT文档中的文本内容 |
| **2. 结构化信息抽取** | Qwen / GPT-4-turbo | 提取关键参数（功率、电压、通信协议、接口定义等）并生成结构化JSON数据 |
| **3. 向量化与索引** | BGE-M3 / SentenceTransformers + Milvus | 将文档语义向量化并存储，实现高效语义搜索 |
| **4. 关键词索引与匹配** | Elasticsearch (BM25) | 建立稀疏索引，用于关键词检索和精确匹配 |
| **5. 知识问答与Agent对话系统** | LangChain Agent + LangGraph | 实现智能问答和任务型多轮对话（如“告诉我MCP9700的工作温度”） |
| **6. 数据存储层** | MongoDB | 存储原始文档、结构化字段和上下文信息 |
| **7. 前端交互** | Streamlit | 上传文件、输入查询、查看Agent对话结果 |
| **8. 性能日志** | Loguru + asyncio | 提供异步处理与日志追踪，提高并发性能 |

---

### ⚙️ 系统工作流程

![SystemFlow](F:\KeyWordSystem\SystemFlow.png)

```
📁 上传IoT文档（PDF/DOCX/JPG）
        ↓
🔍 文本解析与OCR提取
        ↓
🧠 LLM抽取结构化参数（功率、电压、温度范围、通信方式等）
        ↓
🔢 向量生成（BGE-M3 Embedding）
        ↓
💾 存储：Milvus（语义向量） + Elasticsearch（关键词索引） + MongoDB（原始与结构化内容）
        ↓
💬 用户查询（自然语言或技术指令）
        ↓
🔗 混合检索 → 召回上下文
        ↓
🧠 LLM生成答案（基于上下文）
        ↓
🗣️ LangChain Agent多轮对话（支持上下文记忆与追问）
```

---

### 🧠 多轮智能问答示例
```
用户：请告诉我MCP9700传感器的温度范围。
系统：MCP9700的温度检测范围为 -40°C 到 +125°C。
用户：那它的输出电压是多少？
系统：在25°C下输出电压约500mV，每升高1°C增加10mV。
用户：请帮我找出所有支持LoRa的模块。
系统：已找到3个模块：RAK3172、E78-900M22S、Wio-E5。
```

---
### 🧪 备用评估方法
使用 Ragas 框架对问答进行：
- **忠实度（Faithfulness）**
- **相关性（Answer Relevance）**
- **上下文召回率（Context Recall）**
- **上下文精确率（Context Precision）**
---

### 🧰 技术栈汇总
```
- Backend: Python 3.10+, LangChain, LangGraph, FastAPI
- LLM: Qwen / GPT-4-turbo
- Embedding: BGE-M3
- DB: MongoDB, Milvus, Elasticsearch
- UI: Streamlit
- Evaluation: Ragas
```
class IoTDocProcessor:
    """
    IoT 文档五步处理流水线：
    1. 文本提取 (Marker / PyMuPDF)
    2. 内容验证 (检查是否为IoT相关文档)
    3. 语义分析 (AI模型提取关键参数与关系)
    4. 向量索引 (LangChain + Ollama)
    5. 数据入库 (保存为结构化JSON或数据库)
    """

    def process_uploaded_file(self, uploaded_file, project_id, description):
        """处理上传的 IoT 技术文档（完整流程）"""
    
        result = {
            'steps': {
                'extract': False,   # 步骤1: 文本提取
                'validate': False,  # 步骤2: 内容验证
                'analyze': False,   # 步骤3: AI语义分析
                'index': False,     # 步骤4: 向量索引
                'save': False       # 步骤5: 保存数据
            }
        }
    
        # Step 1: 文本提取 (PDF / Word / 图片)
        text, extract_success = self.extract_text(uploaded_file)
        result['steps']['extract'] = extract_success
        if not extract_success:
            return False, "❌ 文件解析失败", result
    
        # Step 2: 内容验证（判断是否为IoT设备文档）
        is_valid = self.validate_iot_content(text)
        result['steps']['validate'] = is_valid
        if not is_valid:
            return False, "⚠️ 文件内容疑似不是 IoT 文档", result
    
        # Step 3: AI语义分析（参数、模块、协议）
        analysis, analyze_success = self.analyze_with_ai(text, description)
        result['steps']['analyze'] = analyze_success
    
        # Step 4: 向量索引（入LangChain / Ollama 向量库）
        index_success = self.build_vector_index(uploaded_file, project_id)
        result['steps']['index'] = index_success
    
        # Step 5: 保存结构化数据
        profile = self.create_iot_profile(uploaded_file, analysis)
        record_id = self.data_store.save(profile, analysis)
        result['steps']['save'] = record_id > 0
    
        return True, "✅ 处理成功", result

## 🚀 Part II：IoT-RAG++ 改进系统 — 混合检索与强化多轮对话Agent

### 🎯 改进目标
在Part I基础上，进一步提升系统的语义理解能力、检索准确性与对话流畅性，实现“**知识级多模态RAG系统**”。

---

### 🔍 改进要点与新增技术

| 改进方向 | 新增技术 | 功能提升 |
|-----------|-----------|-----------|
| **1. 双引擎混合检索增强** | Milvus + Elasticsearch 并行召回 + CrossEncoder 重排 | 提高语义与关键词匹配平衡度，实现精准推荐 |
| **2. CrossEncoder rerank模块** | `cross-encoder/ms-marco-MiniLM-L-12-v2` | 基于相似度打分的精确重排，提升最终Top-N质量 |
| **3. 多轮对话上下文记忆** | LangGraph + session_state | 支持上下文记忆、条件修正与多轮追问 |
| **4. 模块化与异步化重构** | asyncio + 解耦模块 | 提升响应速度与系统可扩展性 |
| **5. 可解释推荐理由生成** | Qwen + JSON模板 | 生成“推荐原因”和“证据来源”，确保可追溯性 |
| **6. LLM硬件需求计算器** | Streamlit + Python计算模型 | 自动估算推理/训练/LoRA微调所需显存和GPU数量 |
| **7. RAG评估模块扩展** | 自定义Ragas Adapter | 支持BGE-M3模型的独立评估与可视化报告输出 |

---

### ⚙️ 改进后的系统流程
```
📁 上传多模态文档
        ↓
🧠 文本抽取 + LLM结构化解析
        ↓
🧮 并行嵌入生成（稠密+稀疏向量）
        ↓
🔍 双引擎混合召回（Milvus + Elasticsearch）
        ↓
🧩 CrossEncoder重排（二次过滤与得分排序）
        ↓
🗣️ LangGraph多轮Agent对话（上下文记忆）
        ↓
🧾 Qwen生成推荐JSON（含理由与来源）
        ↓
📊 Ragas + Streamlit性能评估与硬件计算
```

---

### 🧠 多轮智能问答示例（改进版）
```
用户：请推荐适合温湿度监测的LoRa模块。
系统：推荐 Wio-E5，原因：支持LoRaWAN、低功耗、适配DHT11传感器。
用户：如果我想要BLE连接的版本呢？
系统：推荐 ESP32-C3，原因：集成BLE 5.0 与 WiFi，功耗低。
用户：请输出它们的对比表格。
系统：已生成对比：
| 模块 | 通信协议 | 功耗 | 支持传感器 |
|------|-----------|------|-------------|
| Wio-E5 | LoRaWAN | 0.8mA | DHT11 |
| ESP32-C3 | BLE + WiFi | 0.9mA | DHT11, BME280 |
```

---

### 🧩 技术创新与论文价值点
- **混合检索融合设计**：实现语义与关键词召回的统一策略，解决传统IoT知识问答检索不全的问题。  
- **可解释推荐**：输出推荐理由和证据文件，增强结果可信度。  
- **多轮对话Agent**：具备上下文状态保持与任务追踪，能进行条件修改、追问与细化查询。  
- **RAG系统评估闭环**：形成从知识解析→检索→生成→评估的完整AI工程链。  
- **资源可视化与部署优化**：首次引入LLM显存需求评估工具到IoT领域RAG系统。

---

### 🧰 技术栈汇总
```
- Backend: Python 3.10+, LangChain, LangGraph, asyncio
- LLM: Qwen + CrossEncoder
- Embedding: BGE-M3
- DB: MongoDB + Milvus + Elasticsearch
- Evaluation: Ragas + Custom Adapter
- UI: Streamlit + Chart visualizer
- Utilities: GPU Resource Calculator, Loguru
```

---

## 📘 对比总结：两阶段论文方向一览

| 项目 | IoT-RAG (第一篇) | IoT-RAG++ (第二篇) |
|------|-------------------|--------------------|
| 数据格式 | 多模态文档解析 | 多模态+结构化融合 |
| 检索方式 | 单一RAG检索（向量+关键词） | 混合召回 + CrossEncoder重排 |
| 对话功能 | 单轮问答 + 简单追问 | 多轮上下文对话 + 条件修正 |
| 模型 | Qwen + BGE-M3 | Qwen + CrossEncoder + LangGraph |
| 数据库 | MongoDB + Milvus + Elasticsearch | 同上（异步优化+缓存） |
| 评估指标 | Ragas标准评估 | Ragas自定义适配 + 可视化报告 |
| 论文主题建议 | IoT文档的多模态语义检索系统 | 基于混合RAG与多轮Agent的智能推荐系统 |

---

## 📄 推荐论文题目（建议用）
1. **Part I:**  
   *“Implementation of Multi-Modal IoT Knowledge Retrieval System Based on RAG and Intelligent Agent”*

2. **Part II:**  
   *“Enhanced IoT-RAG++: Hybrid Semantic Retrieval and Multi-turn Conversational Agent for Explainable Recommendation”*

---
