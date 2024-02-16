import datetime
import time
import os.path
import streamlit as st 
from langchain_community.llms import Ollama
from langchain.callbacks import get_openai_callback
from waiting import wait

# Import script for downloading models
from download_model import download
# Import script for removing models
from remove_model import remove

# For storing and handling past chats
class Chat:

    # Constructor
    def __init__(self, messages):
        self.messages = messages  # Chat history (both prompts and responses)
        self.timestamp = datetime.datetime.now()  # Timestamp for last edit
        
        f = open('chat_ids.txt','r')
        lines = f.readlines()
        self.chat_id = len(lines)
        f.close()

    # Add a new message (prompt or response) to messages
    def add_message(self, messages):
        self.messages = messages
        self.update_timestamp()
        self.update_chat_log()

    # Update the timestamp to current time
    def update_timestamp(self):
        self.timestamp = datetime.datetime.now()

    # Update the chat log of current chat
    def update_chat_log(self):
        self.update_timestamp()
        f = open('ChatLogs/chatlog_' + str(self.chat_id) + '.txt', 'w')
        f.write(str(self.timestamp))
        messages = self.messages
        f.write('\n' + str(messages))
        f.close()

# Response generation
def generate_response(prompt, history):

    # Create a prompt chain using past prompts and responses
    prompt_chain = ""
    for log in history:
        prompt_chain += " " + log["content"]

    # Return the response from the llm
    with get_openai_callback() as cb:
        result = llm.invoke(prompt_chain)
    return result, cb

# Create new chat
def new_chat():

    f = open('chat_ids.txt','a')
    f.write("X\n")
    f.close()

    if 'current_chat' in globals():
        current_chat.update_chat_log()

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

# Empty llm list for storing llms
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

# Create and name tabs
tab1, tab2 = st.tabs(["Chat", "Model Manager"])

# Save the llm as an Ollama object
llm = Ollama(model = select)

# In the chat tab:
with tab1:
    # Prompt the user 
    prompt = st.chat_input("Enter prompt:")
    response = ""
    st.write("")
    st.write("")

    # New chat button
    if st.button("NEW CHAT", key="button"):
        current_chat = new_chat()

    # After the user hits enter or clicks the send button
    if prompt:

        if 'current_chat' not in globals():
            current_chat = Chat("")

        # Start the response timer
        start_time = time.time()
        
        # Add the prompt to the chat history as a user prompt
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Update current chat's message history
        current_chat.add_message(st.session_state.messages)

        with st.spinner('Generating reponse...'):
            # Use generate_response method to create a response
            response, callback = generate_response(prompt, st.session_state.messages)

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
        #st.info(current_chat.messages)

        st.info(callback)

# In the model management tab:
with tab2:

    # Allow user to download a new model
    new_model = st.chat_input("Download a new model? [model-name:version]")
    if new_model:
        with st.spinner('Downloading ' + new_model + "..."):
            # Use download function from download_model.py
            status = download(new_model)
            # Wait for model to download with a 30 minute timeout
            wait(lambda: status, timeout_seconds = 1800, waiting_for="download")
            # Write model name to a model list text file
            f = open('model_list.txt', 'a')
            f.write(new_model)
            f.close()
        if status:
            st.success('Done!')
        else:
            st.faulure('Problem downloading model')
        time.sleep(2)
        st.rerun()


    # Remove model button
    if st.button("REMOVE CURRENTLY SELECTED MODEL", key="button2"):
        with st.spinner('Removing ' + select + "..."):
            # Use remove function to remove currently selected model
            status = remove(select)
        if status:
            st.success('Done!')
        else:
            st.faulure('Could not remove')
        time.sleep(2)
        st.rerun()


# In the sidebar:     
#with st.sidebar:
#    num = 0
#    for element in os.listdir('ChatLogs/'):
#        f = open('ChatLogs/' + element, 'r')
#        lines = f.readlines()
#        c = st.container()
#        with st.chat_message(lines[1]):
#            st.markdown(lines[1])     



