FROM python:3.9.5-slim
ENV HOME /root
WORKDIR /root

COPY . .

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
RUN pip3 install -r requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && pip install gevent-websocket
CMD /wait && python -u app.py