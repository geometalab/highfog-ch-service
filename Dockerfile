FROM nginx:alpine

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./nginx/nginx.conf.template /etc/nginx/conf.d/default.conf.template
RUN rm -rf /docker-entrypoint.d
COPY ./nginx/50-setup-templates.sh /docker-entrypoint.sh

COPY frontend /var/www

EXPOSE 80

CMD ["nginx" "-g" "daemon off;"]
