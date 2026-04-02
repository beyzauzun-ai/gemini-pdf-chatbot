import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
from PyPDF2 import PdfReader

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

if not api_key:
    st.error("GEMINI_API_KEY bulunamadı.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("PDF yükle", type="pdf")

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Bir şey sor...")

if prompt:
    full_prompt = pdf_text + "\n\n" + prompt

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        answer = response.text if response.text else "Yanıt alınamadı."
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
