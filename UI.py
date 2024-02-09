# CURRENT MAIN OBJECTIVE
# Allow for downloading different model versions
# Download polish
# Allow for switching versions of a model
# (remove current automatic :latest usage and update downloading to take suffix into acount)
# > still remove suffix when in dropdown - change it from llama2:latest to llama2 (latest) for example
# Add option to delete models
# Add functionality to check if selected model is not downloaded properly, and download it if this is the case
# ^ This can eventually include scanning website for new updates
# ^ Try to scan website for model names to make installing easier anyways


# NEXT MAIN OBJECTIVE
# Figure out how to have multiple chat histories and how to save them even
# when the app is closed. Likely will use a sidebar that allows the user
# to look through chats, name them, delete them, see how much space they
# take up, and when they were last used. Find a way to display time to run
# under each prompt call as well as a total at the bottom. Find a way to
# display which model was used for a response in the case of multiple
# models being used in a single chat history.

# ^ Currently saves history to a chat object
# need to add way to write to file
# need to add way to name the chat
# etc etc

import time
import os.path
import streamlit as st 
from datetime import date
from langchain_community.llms import Ollama
from waiting import wait

# Import script for donwloading models
from download_model import download

# For storing and handling past chats
class Chat:

    # Constructor
    def __init__(self, messages):
        self.messages = messages  # Chat history (both prompts and responses)

    # Add a new message (prompt or response) to messages
    def add_message(self, messages):
        self.messages = messages

# Create an empty placeholder Chat object
current_chat = Chat("")

# Response generation
def generate_response(prompt, history):

    # Create a prompt chain using past prompts and responses
    prompt_chain = ""
    for log in history:
        prompt_chain += " " + log["content"]

    # Return the response from the llm
    return llm.invoke(prompt_chain)

# Create new chat
def new_chat():

    # Clear the session state messages
    st.session_state.messages = []

    # Create and return a new chat
    chat = Chat(st.session_state.messages)
    return chat    

# Initialize chat history
if "messages" not in st.session_state:
    current_chat = new_chat()

# Company logo
st.image('RSLogo.png')

# Application title
st.title("Generative AI Coding Chat")

llm_list = []

# Open the llm file and save each llm to llm_list
with open('model_list.txt') as file:
    llm_list = file.readlines()

index = 0
# For each llm in the file:
for option in llm_list:
    # Strip the \n elements
    llm_list[index] = option.strip().replace('\n', '')
    index += 1

# Select the llm
select = st.selectbox("Select Model: ", llm_list)

# Allow user to download a new model
new_model = st.chat_input("Download a new model?")
if new_model:
    # Use download function from download_model.py
    status = download(new_model)
    # Wait for model to download with a 30 minute timeout
    wait(lambda: status, timeout_seconds = 1800, waiting_for="download")
    # Write model name to a new file
    f = open('model_list.txt', 'a')
    f.write("\n" + new_model)
    f.close()

# Ensure that the model variation is latest
# selected_model = select + ":latest"

# -Deletion involves a different call and will be handled later
# -Model updating should be looked into as well
# -Finding a way to automatically find which models ollama offers, as well as information
#   about them should be researched.
# -An alternate way of downloading and loading llms may also be useful, although Ollama
#   seems to be the most practical at the time being. Having multiple options can not hurt.

# Save the llm as an Ollama object
llm = Ollama(model = select)

# Prompt the user 
prompt = st.chat_input("Enter prompt:")
response = ""
st.write("")
st.write("")

# New chat button
if st.button("CLEAR HISTORY", key="button"):
    current_chat = new_chat()

# After the user hits enter or clicks the send button
if prompt:

    # Start the response timer
    start_time = time.time()
    
    # Add the prompt to the chat history as a user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Update current chat's message history
    current_chat.add_message(st.session_state.messages)

    with st.spinner('Generating reponse...'):
        # Use generate_response method to create a response
        response = generate_response(prompt, st.session_state.messages)

        # Add the response to the chat history as an assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Update current chat's message history
        current_chat.add_message(st.session_state.messages)

        # Display chat messages from history, as well as new response
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # End the response timer, evaluate time to finsish, and output result
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_message = f"Model took {elapsed_time} seconds to respond"
    st.success(time_message)

    # Print currently store chat messages
    st.info(current_chat.messages)