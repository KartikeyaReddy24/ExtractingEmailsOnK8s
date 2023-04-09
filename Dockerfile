FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y git

RUN git clone https://github.com/KartikeyaReddy24/ExtractingEmails.git

WORKDIR /ExtractingEmails

RUN apt-get install -y python3-pip

RUN pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install googlesearch-python

RUN python3 -m pip install xlsxwriter

CMD [ "python3", "ExtractEmails_v2.6.py" ]
