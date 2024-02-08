import time
import streamlit as st 
from langchain_community.llms import Ollama

# Save the llm as an Ollama object
llm = Ollama(model="deepseek-coder:latest")

# Application title
st.title("RiteSolutions GenAI Chat")

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

if st.button("CLEAR HISTORY", key="button"):
        empty_history()

# After the user hits enter or clicks the send button
if prompt:

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
    elapsed_time = end_time - start_time
    time_message = f"Model took {elapsed_time} seconds to respond"
    st.success(time_message)
