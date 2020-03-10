FROM ubuntu:latest

RUN apt-get update -y &&\
    apt-get install python3 -y &&\
    apt-get clean -y &&\
    apt-get install libxml2-dev -y libxslt1-dev -y libssl-dev -y &&\
    apt install python3-pip -y &&\
    apt-get install python3-dev -y &&\
    apt-get install libmysqlclient-dev -y &&\
    apt-get install libsasl2-dev libldap2-dev libssl-dev -y

COPY nonexternalprocess/ /app
workdir /app
EXPOSE 8050

RUN apt-get clean &&\
    apt-get update &&\
    pip3 install -r requirements.txt  

CMD ["python3", "external_process.py"]
