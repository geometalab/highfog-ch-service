FROM python:2.7

LABEL maintainer="Geometalab <geometalab@hsr.ch>"

RUN apt-get update \ 
    && apt-get install -y wget libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

ENV DOCKERIZE_VERSION v0.6.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENV PYTHONUNBUFFERED=non-empty-string PYTHONIOENCODING=utf-8 LC_ALL=C.UTF-8 LANG=C.UTF-8

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /highfog

WORKDIR /highfog

EXPOSE 8080

ENV PYTHONPATH=${PYTHONPATH}:/highfog

CMD ["uwsgi", "--chdir", "/highfog/", "--http", "0.0.0.0:8080", "--wsgi-file", "highfog.wsgi"]
