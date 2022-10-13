from flask import request, Flask

app = Flask("project name")


@app.route('/', methods=['GET'])
def hello():
    return "hello"
