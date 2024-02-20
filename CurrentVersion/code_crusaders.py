import importlib.util
import os

# Dependencies to check/download
package_names = ['streamlit', 'langchain_community', 'waiting', 'ollama', 'tqdm']

print ("--- Checking for dependencies ---")

# Check if dependency is present and download if not
for package in package_names:
    spec = importlib.util.find_spec(package)
    if spec is None:
        print(package + " is not installed")
        print("installing package")
        call = 'pip install ' + package + ' --break-system-packages'
        os.system(call)
    else:
        print(package + " installed")

        # Uncomment below to add auto-updates

        #print(package + " installed, updating if needed")
        #call = 'pip install ' + package + ' --upgrade --break-system-packages'
        #os.system(call)

print ("\n--- Checking for Ollama ---")

# Path for ollama installation
path = '/usr/local/bin/ollama'

# Check if ollama is present
isExisting = os.path.exists(path)

# If ollma is not present, install it
if isExisting == False:
    print("Ollama is not installed")
    print("installing Ollama")
    call = 'curl https://ollama.ai/install.sh | sh'
    os.system(call)
else:
    print("Ollama is installed")

print ("\n--- Running WebUI ---")

# Run the main script using a system call
call = 'streamlit run UI.py'
os.system(call)
