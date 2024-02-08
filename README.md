# CodeCrusaders
Using Local LLMs to Support Software Development and Test

Planned Changes:
    - Change current process of having one chat log that has a deleting history
    to a process that allows the user to have multiple chat histories, being 
    able to save them to files for export and switch between them in app
    - Integrate drop down to select llm with current version of ui that allows
    for chat history
        - State which llm operated on each chat within chat history for context
        and clarity
    - Improve aestheics
    - Possibly make a function that looks for and copies generated code into a
    matching file type, runs it, and reports errors
    - Automatic tracking of metrics
        - If able to track if errors occur in generated code:
            - Return what type of error to see if llms frequent the same error

Installation (Will be improved at a later date):
    For linux or wsl:
    enter 'curl https://ollama.ai/install.sh | sh' in terminal to install Ollama
    enter 'ollama run <model:version> to install model (e.g. ollama run deepseek-coder-latest)
    enter /bye to close llm, it is now downloaded for future use
    use pip to install streamlit and langchain-community (pip install streamlit langchain-community)
    run the application by entering 'streamlit run UI.py'
