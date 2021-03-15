FROM python:3.8-rc-alpine

COPY ./requirements.txt /requirements.txt
COPY ./index.py /index.py
RUN pip install -r requirements.txt