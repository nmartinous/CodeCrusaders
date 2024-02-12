import os

# Function to download model
def remove(model_name):

    found = 0

    with open(r'model_list.txt', 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            if line.find(model_name) != -1:
                found = line

    with open(r'model_list.txt', 'w') as fp:
        for number, line in enumerate(lines):
            if number not in [-1, found]:
                fp.write(line)

                # Create a system call to remove selected model
                call = 'ollama rm ' + str(model_name)
                status = os.system(call)

                # Tell the main script the remove status
                if status == 0:
                    return True
                else:
                    return False
            else:
                return False
