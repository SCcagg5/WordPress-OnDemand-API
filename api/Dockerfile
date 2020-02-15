FROM ubuntu

LABEL maintainer="Courtel Eliot"
LABEL maintainermail="eliot.courtel@wanadoo.fr"

WORKDIR /home/api
RUN apt upgrade && apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.7 -y
RUN apt install python3-pip -y
RUN python3.7 -m pip install pip

ENTRYPOINT \
	   pip3 install --upgrade pip && \
	   pip install --upgrade -r requirements.txt && python3 server.py;
