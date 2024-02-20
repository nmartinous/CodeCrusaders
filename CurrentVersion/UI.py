# IMPORTS
# ------------------------------------------------------

import time
import streamlit as st 
from ollama import chat, pull
from tqdm import tqdm

########################################################
# TITLE AND LOGO
# ------------------------------------------------------

# Company logo
st.image('RSLogo.png')

# Application title
st.title('Generative AI Coding Chat')

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

    # After the user hits enter 
    if prompt:
        with st.spinner('Generating Response...'):
            # Add the prompt to chat history
            st.session_state.chat_history.append({'role': 'user', 'content': prompt})
            # Generate a response using the full chat history
            response = chat(model, messages=st.session_state.chat_history)
            # Display the response
            st.markdown(response['message']['content'])
            # Add the response to the chat history
            st.session_state.chat_history.append(response['message'])
            # Output run stats
            st.info('Total Response Time: ' + str(response['total_duration']/1000000000) 
                    + '\n\nLoad Time: ' + str(response['load_duration']/1000000000)
                    + '\n\nPrompt Evals: ' + str(response['prompt_eval_count']) 
                    + '\n\nPrompt Eval Time: ' + str(response['prompt_eval_duration']/1000000000)
                    + '\n\nPrompt Eval Tokens Per Second: ' + str((int(response['prompt_eval_duration']/1000000000))/int(response['prompt_eval_count']))
                    + '\n\nEvals: ' + str(response['eval_count'])
                    + '\n\nEval Time: ' + str(response['eval_duration']/1000000000)
                    + '\n\nEval Tokens Per Second: ' + str((int(response['eval_duration']/1000000000))/int(response['eval_count'])))


########################################################
# MODEL MANAGEMENT TAB
# ------------------------------------------------------

with tab2:
    new_model = st.chat_input("Download a new model? [model-name:version]")
    if new_model:

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

