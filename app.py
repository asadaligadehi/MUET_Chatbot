import streamlit as st
from chatbot.rag_chatbot import ask_question

st.set_page_config(page_title="MUET AI Chatbot", layout="wide")

st.title("MUET AI Chatbot")
st.write("Ask questions about Mehran University")

user_input = st.text_input("Ask a question")

if st.button("Ask"):

    if user_input:
        with st.spinner("Thinking..."):

            answer = ask_question(user_input)

        st.success("Answer")
        st.write(answer)