FROM python:3

ADD app.py /

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python", "-u", "server.py", "database.py" ]