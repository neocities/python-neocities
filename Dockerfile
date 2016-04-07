FROM python:2.7
MAINTAINER AJ Bowen <aj@soulshake.net>

RUN mkdir /src
COPY . /src
WORKDIR /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade .
ENTRYPOINT ["nc.py"]
