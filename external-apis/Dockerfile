FROM python:3.8-alpine
WORKDIR /app
RUN apk add postgresql-dev gcc python3-dev musl-dev openssl-dev cargo libffi-dev postgresql-client git make mariadb-dev libxml2-dev libxslt-dev
RUN pip install uwsgi
COPY . .
RUN pip install -e /app
RUN chmod +x /app/etc/docker/wait-for-command.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
