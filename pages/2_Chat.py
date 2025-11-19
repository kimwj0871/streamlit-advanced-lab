import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="Chat", page_icon="💬")

# 제목
st.title("💬 Chat - 대화형 챗봇")

# OpenAI API 키 입력
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# 세션 상태에 대화 저장 (streamlit이 새로고침되어도 기록 유지)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 이전 대화 표시
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
user_input = st.chat_input("메시지를 입력하세요:")

# GPT 응답 처리
if user_input:
    if not api_key:
        st.warning("API 키를 입력하세요!")
    else:
        # 사용자 메시지 저장
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # OpenAI 클라이언트 생성
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_input
        )

        # GPT 응답 텍스트 추출
        gpt_reply = response.output[0].content[0].text

        # GPT 메시지 저장
        st.session_state["messages"].append({"role": "assistant", "content": gpt_reply})

        # GPT 메시지 출력
        with st.chat_message("assistant"):
            st.write(gpt_reply)
