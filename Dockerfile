FROM python:3.8
USER root
WORKDIR /home

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN apt-get update
RUN apt-get install -y vim ffmpeg
RUN pip install numpy matplotlib ipython
