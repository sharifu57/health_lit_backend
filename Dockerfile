FROM python:3.12.0
LABEL Name=health Version=1.0

RUN mkdir /health
WORKDIR /health
ADD requirements.txt /health/
RUN pip install -r requirements.txt
EXPOSE 8000

