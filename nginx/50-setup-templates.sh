#!/bin/sh

set -e

domain_subst() {
    DOMAIN_NAMES=$(echo $VIRTUAL_HOST | sed 's/,/ /g') envsubst '$DOMAIN_NAMES' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
}

create_config() {
    envsubst < /var/www/js/config.template.js > /var/www/js/config.js
}

domain_subst
create_config

exec "$@"
