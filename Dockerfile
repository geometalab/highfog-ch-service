FROM nginx:alpine

COPY ./nginx/nginx.conf.template /etc/nginx/conf.d/default.conf.template

COPY frontend /var/www

CMD DOMAIN_NAMES=$(echo $VIRTUAL_HOST | sed 's/,/ /g') envsubst '$DOMAIN_NAMES' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf \
    && envsubst < /var/www/js/config.template.js > /var/www/js/config.js \
    && nginx -g 'daemon off;'
