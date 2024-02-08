import time
import streamlit as st 
from langchain_community.llms import Ollama
llm = Ollama(model="tinyllama:latest")

st.title("RiteSolutions GenAI Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

colA, colB = st.columns([.99, .01])
with colA:
    prompt = st.chat_input("Enter prompt:")
    response = ""
    st.write("")
    st.write("")
    if prompt:
        start_time = time.time()
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = llm.invoke(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_message = f"Model took {elapsed_time} seconds to respond"
        st.success(time_message)