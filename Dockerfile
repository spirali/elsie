FROM ubuntu:20.04

# Global dependencies
RUN apt-get update &&\
    apt-get install -y --no-install-recommends software-properties-common

RUN add-apt-repository ppa:inkscape.dev/stable &&\
    apt-get update &&\
    apt-get install -y --no-install-recommends python3 python3-pip inkscape=1:1.2.1+202207142221+cd75a1ee6d~ubuntu20.04.1

RUN pip3 install -U pip setuptools wheel

WORKDIR /elsie

# Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN pip3 install .[cairo]

WORKDIR /slides
