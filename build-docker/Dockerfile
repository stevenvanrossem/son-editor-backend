FROM pgsandman2016/upb-son-editor-backend-base:v1

#install infconfig
RUN apt-get update
RUN apt-get install -y net-tools

#install the son-editor-frontend
RUN git clone https://github.com/sonata-nfv/son-editor-frontend /var/www/
COPY ./constants.js /var/www/js/constants.js

#install the son-editor-backend
RUN rm -rf /app
RUN git clone https://github.com/sonata-nfv/son-editor-backend.git /app
WORKDIR /app
RUN pip install -e .
COPY ./config.yaml /app/src/son_editor/config.yaml

# load nginx config
COPY ./nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./uwsgi.ini /app/uwsgi.ini


EXPOSE 80
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 777 entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
