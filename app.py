# app.py
import streamlit as st
from rag_engine import rag_answer

st.set_page_config(page_title="IoT 集成助手", layout="wide")

st.title("🔌 IoT 设备集成 / 配线 / SEMAR 接入助手 (本地RAG)")
st.write("离线运行 · 基于你的PDF规格书和接线手册 · 引用具体页码作为证据")

user_question = st.text_area(
    "请输入你的需求 / 场景描述（例如：我要用低功耗温湿度传感器监测机房，并上传到树莓派网关）：",
    height=120
)

if st.button("生成建议"):
    if not user_question.strip():
        st.warning("请先输入问题")
    else:
        result = rag_answer(user_question)

        # 左列：答案
        left, right = st.columns([2,1])

        with left:
            st.subheader("💡 建议 / 步骤")
            st.write(result["answer"])

            st.markdown("**引用证据 (文件 / 页码):**")
            for ev in result["evidence"]:
                st.markdown(f"- {ev['file']} p.{ev['page']}")

        # 右列：原文片段
        with right:
            st.subheader("📄 参考片段")
            for i, doc in enumerate(result["raw_docs"], start=1):
                with st.expander(f"片段 {i}: {doc['source']}"):
                    st.text(doc["content"])
