import streamlit as st
from openai import OpenAI

# 🔧 페이지 기본 설정
st.set_page_config(page_title="GPT Response", page_icon="🤖")

# 🎯 제목
st.title("🤖 GPT Response")

# 🔑 API 키 입력
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# 💬 질문 입력
user_input = st.text_area("질문을 입력하세요:")

# ✨ 버튼 클릭 시 응답
if st.button("답변 보기"):
    if not api_key:
        st.warning("API 키를 입력하세요!")
    elif not user_input.strip():
        st.warning("질문을 입력하세요!")
    else:
        try:
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model="gpt-4o-mini",
                input=user_input
            )
            st.success("🧠 GPT의 답변:")
            st.write(response.output[0].content[0].text)
        except Exception as e:
            st.error(f"오류 발생: {e}")
