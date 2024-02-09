import time
import streamlit as st 
from langchain_community.llms import Ollama

# Application title
st.title("RiteSolutions GenAI Chat")

# Save the llm as an Ollama object
select = st.selectbox("Model: ", ["Select","tinyllama", "llama2", "deepseek-coder:latest"])
llm = Ollama(model = select)
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

# Collapses chat history
def collapse_history():
    if "Select" not in st.session_state.saved_prompts:
        st.session_state.saved_prompts.append("Select")
    for message in st.session_state.messages:
        if message["role"] == "user" and message["content"] not in st.session_state.saved_prompts:
            st.session_state.saved_prompts.append(message["content"])
    selected_prompt = st.selectbox("Previous Prompts", st.session_state.saved_prompts)
    if selected_prompt != "Select":
        # Clear existing messages
        st.session_state.messages = []
        # Iterate through saved messages and add those that match the selected prompt
        for message in st.session_state.saved_messages:
            if message["content"] == selected_prompt:
                st.session_state.messages.append({"role": "user", "content": message["content"]})
                st.session_state.messages.append({"role": "assistant", "content": message["response"]})
        # Display chat messages from history, as well as new response
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

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

if st.button("COLLAPSE HISTORY", key="collapse_button"):
    collapse_history()
    

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
    elapsed_time = round(end_time - start_time,2)
    time_message = "Model took " + str(elapsed_time) +" seconds to respond"
    st.info(time_message)
