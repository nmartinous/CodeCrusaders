import os

# Function to download model
def download(model_name):

    # Create a system call to pull selected model
    call = 'ollama pull ' + model_name
    status = os.system(call)

    # Tell the main script the download status
    if status == 0:
        return True
    else:
        return False




