FROM python:3-stretch

LABEL maintainer="Geometalab <geometalab@hsr.ch>"

RUN apt-get update
RUN apt-get install -y gdal-bin python-gdal

ENV RESULT_TIF=/tmp/area.tif

COPY . /code

WORKDIR /code

