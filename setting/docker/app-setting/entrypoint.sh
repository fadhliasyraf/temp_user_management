#!/bin/bash

# Replace placeholders in uWSGI config
sed -i "s|{{URL_PROD}}|${URL_PROD}|g" /tmp/uwsgi.ini
sed -i "s|{{SHORT_REQUEST_SEC}}|${SHORT_REQUEST_SEC}|g" /tmp/uwsgi.ini
sed -i "s|{{LONG_REQUEST_SEC}}|${LONG_REQUEST_SEC}|g" /tmp/uwsgi.ini

# Replace placeholders in Nginx config using envsubst
envsubst '${URL_PROD} ${SHORT_REQUEST_SEC} ${LONG_REQUEST_SEC}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

exec /usr/local/bin/supervisord -c /usr/local/etc/supervisord.conf