FROM python:3.8

WORKDIR /app

COPY requriments.txt ./requriments.txt

RUN pip3 install -r requriments.txt

EXPOSE 8080

COPY . /app

# ENTRYPOINT   ["streamlit","run"]

CMD streamlit run --server.port 8080 --server.enableCORS false base.py
