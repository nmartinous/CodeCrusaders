import os

def download(model_name):
    call = 'ollama pull ' + model_name
    status = os.system(call)
    if status == 0:
        return True
    else:
        return False




