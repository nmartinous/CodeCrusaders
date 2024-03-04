# IMPORTS
# ------------------------------------------------------

from datetime import datetime
import os
import json
import streamlit as st 
from ollama import chat, pull
from tqdm import tqdm
from remove_model import remove

########################################################
# TITLE AND LOGO
# ------------------------------------------------------

# Company logo
st.image('RSLogo.png')

# Application title
st.title('Generative Coding Chat')

########################################################
# CREATE AND MANAGE CHAT HISTORY
# ------------------------------------------------------

# Initialize chat history if one does not exist
if 'chat_history' not in st.session_state:
  st.session_state.chat_history = []

# Structure for user messages:
# {'role': 'user', 'content' : <prompt>}
#
#  - To access message: ['content']
#
# Structure for assistant messages:
# {'role': 'assistant', 'content': {'model': <model>, 
# created_at: <timestamp>, 'message': {'role': 'assistant', 
# 'content': <message>}, 'done': <status bool>,
# 'total_duration': <runtime>, 'load_duration': <model load>,
# 'prompt_eval_count': <??>, 'prompt_eval_duration': <??>,
# 'eval_count': <??>, 'eval_duration': <??>}}
#
#  - To access message: ['content']['message']['content']

########################################################
# ACCESS DOWNLOADED MODELS AND ALLOW USER TO SELECT ONE
# ------------------------------------------------------

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

# Select the llm with a dropdown
model = st.selectbox('Select Model: ', llm_list)

########################################################
# SAVE AND LOAD CHATS
# ------------------------------------------------------

# Save active chat history using timestamp
def save_chat_history():
    now = datetime.now()
    filename = './chat_logs/' + str(now) + '.json'
    if st.session_state.chat_history:  # Check if history exists
        with open(filename, "w") as f:
            json.dump(st.session_state.chat_history, f)

# Load selected filename
def load_chat_history(filename="./chat_logs/chat_history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            st.session_state.chat_history = json.load(f)
    else:
        st.session_state.chat_history = []  # Initialize empty if no file

########################################################
# TAB STRUCTURE
# ------------------------------------------------------

# Create and name tabs
tab1, tab2 = st.tabs(['Chat', 'Model Manager'])

########################################################
# CHAT TAB
# ------------------------------------------------------

with tab1:
    # Prompt the user 
    prompt = st.chat_input('Enter prompt:')
    response = ""
    st.write('')
    st.write('')

    # Button to save chat
    if st.button("Save Chat"):
        save_chat_history()

    uploaded_file = st.file_uploader("Choose a chat history file")
    if uploaded_file:
        load_chat_history(uploaded_file.name)  # Load from temporary file

    # After the user hits enter 
    if prompt:
        with st.spinner('Generating Response...'):
            # Add the prompt to chat history
            st.session_state.chat_history.append({'role': 'user', 'content': prompt})
            # Generate a response using the full chat history
            response = chat(model, messages=st.session_state.chat_history)
            # Display the response
            #st.markdown(response['message']['content'])
            # Add the response to the chat history
            st.session_state.chat_history.append(response['message'])

            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Generate run stats
            total_time = round(response['total_duration']/1000000000, 2)
            load_time = round(response['load_duration']/1000000000, 2)
            if "prompt_eval_count" in response:
                prompt_tokens = response['prompt_eval_count']
                prompt_eval = round(response['prompt_eval_duration']/1000000000, 2)
                prompt_tps = round((response['prompt_eval_duration']/1000000000)/(response['prompt_eval_count']), 2)
            else:
                prompt_tokens = "DATA ERROR"
                prompt_eval = "DATA ERROR"
                prompt_tps = "DATA ERROR"
            response_tokens = response['eval_count']
            response_eval = round(response['eval_duration']/1000000000, 2)
            response_tps = round((response['eval_duration']/1000000000)/(response['eval_count']), 2)

            # Output run stats
            if "prompt_eval_count" in response:
                st.success('Total Response Time: ' + str(total_time) + ' seconds'
                           + '\n\nPrompt Tokens Per Second: ' + str(prompt_eval)
                           + '\n\nGenerated Tokens Per Second: ' + str(response_tps))
                st.info('Load Time: ' + str(load_time) + ' seconds'
                    + '\n\nPrompt Tokens: ' + str(prompt_tokens) 
                    + '\n\nPrompt Eval Time: ' + str(prompt_eval) + ' seconds'
                    + '\n\nResponse Tokens: ' + str(response_tokens)
                    + '\n\nGeneration Time: ' + str(response_eval))
            else:
                st.success('Total Response Time: ' + str(total_time) + ' seconds'
                           + '\n\nPrompt Tokens Per Second: ' + str(prompt_eval)
                           + '\n\nGenerated Tokens Per Second: ' + str(response_tps))
                st.info('Load Time: ' + str(load_time) + ' seconds'
                    + '\n\nPrompt Tokens: ' + str(prompt_tokens) 
                    + '\n\nPrompt Eval Time: ' + str(prompt_eval)
                    + '\n\nResponse Tokens: ' + str(response_tokens)
                    + '\n\nGeneration Time: ' + str(response_eval))


########################################################
# MODEL MANAGEMENT TAB
# ------------------------------------------------------

with tab2:
    new_model = st.chat_input("Download a new model? [model-name:version]")
    if new_model:
        with st.spinner('Downloading ' + new_model + '...'):
            current_digest, bars = '', {}
            for progress in pull(new_model, stream=True):
                digest = progress.get('digest', '')
                if digest != current_digest and current_digest in bars:
                    bars[current_digest].close()

                if not digest:
                    print(progress.get('status'))
                    continue

                if digest not in bars and (total := progress.get('total')):
                    bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

                if completed := progress.get('completed'):
                    bars[digest].update(completed - bars[digest].n)

                current_digest = digest
            
            f = open('model_list.txt', 'a')
            f.write(new_model + '\n')
            f.close()

            st.rerun()

    if st.button('REMOVE CURRENTLY SELECTED MODEL'):
        remove(model)
        st.rerun()

with st.sidebar:
    pass

    

