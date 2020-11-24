FROM nginxinc/nginx-unprivileged:1.18-alpine
#FROM nginx:1.19.4-alpine
COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER nginx
