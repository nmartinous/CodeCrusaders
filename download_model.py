import os

# Function to download model
def download(model_name):

    found = False

    with open(r'model_list.txt', 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            if line.find(model_name) != -1:
                found = True

    if found == False:
        # Create a system call to pull selected model
        call = 'ollama pull ' + model_name
        status = os.system(call)

        # Tell the main script the download status
        if status == 0:
            return True
        else:
            return False
                

   