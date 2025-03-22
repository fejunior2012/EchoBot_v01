# pip install streamlit langchain-openai
# pip install streamlit
# pip install openai

import openai
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

st.title("🦜🔗 Suporte à GSE")

openai_api_key = st.secrets["OPENAI_API_KEY"]

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=openai_api_key)

client = openai.OpenAI(api_key=openai_api_key)

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    st.info(model.invoke(input_text))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app return
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
# React to user input
prompt = st.chat_input("Qual sua necessidade?")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

   
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response_stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        for response in response_stream:
            if response.choices and response.choices[0].delta.content:
                full_response += response.choices[0].delta.content  # Correção aqui
                message_placeholder.markdown(full_response + "▌")  # Indicador de digitação

        message_placeholder.markdown(full_response)  # Exibe resposta final

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    

