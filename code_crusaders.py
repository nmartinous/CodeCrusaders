import importlib.util
import os

package_names = ['streamlit', 'langchain_community', 'waiting']

print ("--- Checking for dependencies ---")

for package in package_names:
    spec = importlib.util.find_spec(package)
    if spec is None:
        print(package + " is not installed")
        print("installing package")
        call = 'pip install ' + package + ' --break-system-packages'
        os.system(call)
    else:
        print(package + " installed")

print ("\n--- Checking for Ollama ---")

path = '/usr/local/bin/ollama'

isExisting = os.path.exists(path)

if isExisting == False:
    print("Ollama is not installed")
    print("installing Ollama")
    call = 'curl https://ollama.ai/install.sh | sh'
    os.system(call)
else:
    print("Ollama is installed")

print ("\n--- Running WebUI ---")
call = 'streamlit run UI.py'
os.system(call)
