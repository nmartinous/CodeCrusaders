import time
import streamlit as st 
from langchain_community.llms import Ollama

# Application title
st.title("RiteSolutions GenAI Chat")


# Save the llm as an Ollama object
select = st.selectbox("Model: ", ["Select","tinyllama", "llama2", "deepseek-coder:latest"])
llm = Ollama(model = select)
select_lang = st.selectbox("Language: ", ["Models Preference","Python", "Java", "C"])

if 'saved_prompts' not in st.session_state:
    st.session_state.saved_prompts = []

# Response generation
def generate_response(prompt, history):

    # Create a prompt chain using past prompts and responses
    prompt_chain = ""
    for log in history:
        prompt_chain += " " + log["content"]

    # Return the response from the llm
    return llm.invoke(prompt_chain)

# Clear chat history
def empty_history():
    st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    empty_history()

# Prompt the user 
prompt = st.chat_input("Enter prompt:")
response = ""
st.write("")
st.write("")

if st.button("CLEAR HISTORY", key="clear_button"):
    empty_history()

# After the user hits enter or clicks the send button
if prompt:

    if select_lang != "Models Preference":
        prompt = prompt + " in "+ select_lang
    
    # Start the response timer
    start_time = time.time()

    # Add the prompt to the chat history as a user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Use generate_response method to create a response
    response = generate_response(prompt, st.session_state.messages)

    # Add the response to the chat history as an assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat messages from history, as well as new response
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # End the response timer, evaluate time to finsish, and output result
    end_time = time.time()
    elapsed_time = round(end_time - start_time,2)
    time_message = "Model took " + str(elapsed_time) +" seconds to respond"
    st.info(time_message)

with st.sidebar:
    i=0
    if st.button("STORE HISTORY", key="store_button"):
        with st.spinner("Loading..."):
            time.sleep(3)
        for message in st.session_state.messages:
            st.session_state.saved_prompts.append(message["role"])
            st.session_state.saved_prompts.append(message["content"])
        for x in range(len(st.session_state.saved_prompts)):
            if x%4 == 1:
                i+=1
                st.button(st.session_state.saved_prompts[x])
                if st.button(st.session_state.saved_prompts[x], key="history_button"+str(i)):
                    empty_history()
                    st.session_state.messages.append({"role": st.session_state.saved_prompts[x-1], "content": st.session_state.saved_prompts[x]})
                    st.session_state.messages.append({"role": st.session_state.saved_prompts[x+1], "content": st.session_state.saved_prompts[x+2]})
