from ollama import chat
import streamlit as st 

# Company logo
st.image('RSLogo.png')

# Application title
st.title('Generative AI Coding Chat')

########################################################

# Initialize chat history
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
# -----------------------------------------------------

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
model = st.selectbox('Select Model: ', llm_list)

########################################################

# Create and name tabs
tab1, tab2 = st.tabs(['Chat', 'Model Manager'])

# In the chat tab:
with tab1:
    # Prompt the user 
    prompt = st.chat_input('Enter prompt:')
    response = ""
    st.write('')
    st.write('')

    # After the user hits enter 
    if prompt:
        st.session_state.chat_history.append({'role': 'user', 'content': prompt})
        response = chat(model, messages=st.session_state.chat_history)
        st.markdown(response['message']['content'])
        st.session_state.chat_history.append(response['message'])

