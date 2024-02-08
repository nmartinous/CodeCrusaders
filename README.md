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
