import streamlit as st 
from langchain_community.llms import Ollama
import time

st.markdown("# Tesing UI")

#llm = Ollama(model="tinyllama") # 👈 stef default
select = st.selectbox("Model: ", ["Select","tinyllama", "llama2", "deepseek-coder:latest"])
llm = Ollama(model = select)

colA, colB = st.columns([.90, .10])
with colA:
    prompt = st.text_input("Enter your prompt", value="", key="prompt")
response = ""
lapsedtime = 0
time_output = "N/A"
with colB:
    st.markdown("")
    st.markdown("")
    if st.button("GO", key="button"):
        start = time.time()
        response = llm.invoke(prompt)
        end = time.time()
        lapsedtime = round(end-start, 2)
        time_output = "The model took " + str(lapsedtime) + " seconds to complete"
st.markdown(response)
st.info(time_output)
