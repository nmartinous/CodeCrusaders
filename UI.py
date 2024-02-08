import time
import streamlit as st 
from langchain_community.llms import Ollama

# Save the llm as an Ollama object
llm = Ollama(model="tinyllama:latest")

# Application title
st.title("RiteSolutions GenAI Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Response generation
def generate_response(prompt, history):

    # Create a prompt chain using past prompts and responses
    prompt_chain = ""
    for log in history:
        prompt_chain += " " + log["content"]

    # Return the response from the llm
    return llm.invoke(prompt_chain)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create two columns, one with 99% width
colA, colB = st.columns([.99, .01])

# In the first column:
with colA:

    # Prompt the user 
    prompt = st.chat_input("Enter prompt:")
    response = ""
    st.write("")
    st.write("")

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

        # Output the response
        st.write(response)

        # End the response timer, evaluate time to finsish, and output result
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_message = f"Model took {elapsed_time} seconds to respond"
        st.success(time_message)
