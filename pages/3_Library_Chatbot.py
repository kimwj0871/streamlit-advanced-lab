import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="Library Chatbot", page_icon="📚")
st.title("📚 Library Chatbot")

# API 키 입력
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# 도서 목록 데이터 (간단 예시)
books = [
    {"title": "파이썬 완벽 가이드", "category": "프로그래밍", "summary": "파이썬의 기초부터 심화까지 다루는 종합서"},
    {"title": "데이터 사이언스 입문", "category": "데이터", "summary": "데이터 분석과 머신러닝의 기초를 설명"},
    {"title": "AI 윤리와 미래 사회", "category": "인공지능", "summary": "AI 시대의 윤리적 쟁점을 다룬 교양서"},
    {"title": "클린 코드", "category": "프로그래밍", "summary": "좋은 코드 작성 원칙과 실무 사례를 제시"},
    {"title": "인공지능의 이해", "category": "인공지능", "summary": "AI의 역사, 원리, 응용을 쉽게 설명"}
]

# 대화 상태 초기화
if "library_messages" not in st.session_state:
    st.session_state["library_messages"] = []

# 이전 대화 표시
for msg in st.session_state["library_messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
user_input = st.chat_input("도서관 챗봇에게 물어보세요:")

# GPT 응답 처리
if user_input:
    if not api_key:
        st.warning("API 키를 입력하세요!")
    else:
        # 사용자 입력 저장
        st.session_state["library_messages"].append({"role": "user", "content": user_input})

        # 도서 추천 로직
        matched_books = [b for b in books if any(keyword in b["category"] or keyword in b["title"] for keyword in user_input.split())]

        if matched_books:
            recommendation = "\n\n".join([f"📘 {b['title']} — {b['summary']}" for b in matched_books])
        else:
            recommendation = "해당 주제에 맞는 도서를 찾을 수 없습니다 😢"

        # GPT 보완 답변 생성
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"사용자가 '{user_input}'라고 물었을 때, 아래 도서 추천 리스트를 참고해서 자연스럽게 대답해줘:\n\n{recommendation}"
        )

        gpt_reply = response.output[0].content[0].text

        # 메시지 기록
        st.session_state["library_messages"].append({"role": "assistant", "content": gpt_reply})

        # 출력
        with st.chat_message("assistant"):
            st.write(gpt_reply)
