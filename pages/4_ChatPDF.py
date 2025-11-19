import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF (PDF 텍스트 추출용)

# 페이지 설정
st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.title("📄 ChatPDF - PDF 문서 기반 챗봇")

# API 키 입력
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# PDF 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요:", type="pdf")

# PDF 텍스트 추출 함수
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

# 업로드 후 텍스트 추출
pdf_text = ""
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF 텍스트 추출 완료!")

# 사용자 질문 입력
user_question = st.text_area("PDF 내용에 대해 질문하세요:")

# GPT 응답
if st.button("답변 보기"):
    if not api_key:
        st.warning("API 키를 입력하세요!")
    elif not uploaded_file:
        st.warning("PDF 파일을 업로드하세요!")
    elif not user_question.strip():
        st.warning("질문을 입력하세요!")
    else:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"다음 PDF 내용 기반으로 질문에 답해줘.\n\nPDF 내용:\n{pdf_text[:6000]}\n\n질문: {user_question}"
        )

        answer = response.output[0].content[0].text
        st.success("🤖 GPT의 답변:")
        st.write(answer)
