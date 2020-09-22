# flask app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hey, We have successfully Dockerized a Flask Web-app'

@app.route('/ping')
def ping():
    return ("", 200)

@app.route('/invocations', methods=["POST"])
def invoke():
    #data = request.get_json(force=True)
    return

if __name__ == '__main__':
    app.run(port=8080)