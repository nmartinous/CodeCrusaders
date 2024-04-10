FROM python:3
COPY . /code_crusaders
WORKDIR /code_crusaders
RUN pip install -r requirements.txt  
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "UI.py", "--server.port=8501", "--server.address=localhost"]
