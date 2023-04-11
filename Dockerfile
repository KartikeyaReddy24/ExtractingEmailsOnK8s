FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y git

RUN git clone https://github.com/KartikeyaReddy24/ExtractingEmailsOnK8s.git

WORKDIR ExtractingEmailsOnK8s

RUN apt-get install -y python3-pip

RUN pip install --upgrade pip

RUN python3 -m pip install googlesearch-python

RUN pip install psycopg2-binary

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "/ExtractingEmailsOnK8s/src/main.py" ]
