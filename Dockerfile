FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 git python3-pip && \
    git clone https://github.com/KartikeyaReddy24/ExtractingEmailsOnK8s.git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ExtractingEmailsOnK8s

RUN pip install --upgrade pip && \
    python3 -m pip install googlesearch-python psycopg2-binary -r requirements.txt

CMD ["python3", "/ExtractingEmailsOnK8s/src/main.py"]
