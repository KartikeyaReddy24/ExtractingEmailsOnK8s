FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 git && \
    git clone https://github.com/KartikeyaReddy24/ExtractingEmailsOnK8s.git && \
    apt-get remove -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ExtractingEmailsOnK8s

RUN apt-get update && \
    apt-get install -y python3-pip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir googlesearch-python psycopg2-binary -r requirements.txt && \
    apt-get purge -y python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime

CMD ["python3", "/ExtractingEmailsOnK8s/src/main.py"]
