FROM python:3.11-slim

RUN apt-get update && apt-get install -y iputils-ping

COPY run.py /

ENTRYPOINT [ "python", "./run.py" ]
