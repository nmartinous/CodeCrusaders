import time
import streamlit as st 
from langchain_community.llms import Ollama

# Select the llm
select = st.selectbox("Select Model: ", ["deepseek-coder", "tinyllama", "llama2"])

# Ensure that the model variation is latest
selected_model = select + ":latest"

# -Add funtionality to choose between sizes, version, as well as download new models
# -Ideally the model selection will be empty on first run and the user will be
#   able to download any model that Ollama supports.
# -This will likely be done by using a text file to keep track of the models the user
#   downloaded so that the user can add and delete models. This file's contents would
#   then be passed as the list for the selectbox above.
# -In order to download new models, an 'Ollama run <model:version> call must be made
#   to the terminal, followed by a '/bye' call to close it. This will likely be handled
#   in a seperate script.
# -Deletion involves a different call and will be handled later
# -Model updating should be looked into as well
# -Finding a way to automatically find which models ollama offers, as well as information
#   about them should be researched.
# -An alternate way of downloading and loading llms may also be useful, although Ollama
#   seems to be the most practical at the time being. Having multiple options can not hurt.

# Save the llm as an Ollama object
llm = Ollama(model = selected_model)

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

# Company logo
st.image('RSLogo.png')

# Application title
st.title("Generative AI Coding Chat")

# Prompt the user 
prompt = st.chat_input("Enter prompt:")
response = ""
st.write("")
st.write("")

# History clearing button
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