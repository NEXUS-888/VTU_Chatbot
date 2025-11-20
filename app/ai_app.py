# app/ai_app.py

import streamlit as st
from ai_bot_core import answer_question

st.set_page_config(
    page_title="VTU Chatbot",
    page_icon="🎓",
    layout="centered",
)

# --- Simple custom CSS ---
st.markdown(
    """
    <style>
    .main {
        background-color: #05030b;
        color: #f5f5f5;
    }
    .block-container {
        max-width: 800px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    .stTextInput>div>div>input {
        background-color: #181824;
        color: #f5f5f5;
        border-radius: 999px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("VTU Chatbot")
st.subheader("CSE 5th Sem · Artificial Intelligence (BCS515B)")

st.write(
    "Ask about **syllabus, modules, exam pattern, course outcomes, or important questions**.\n\n"
    "_Examples:_\n"
    "- `syllabus of module 2`\n"
    "- `what is the exam pattern for ai`\n"
    "- `important questions of module 3`"
)

user_q = st.text_input(
    "Ask your doubt:",
    placeholder="e.g. important questions of module 3",
)

if user_q.strip():
    answer = answer_question(user_q)
    st.markdown("### Answer")
    st.markdown(answer)
