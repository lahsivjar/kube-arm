# Simple flask python app for hello world
from flask import Flask
app = Flask(__name__)

@app.route("/")
def print_hello():
    return "Hello World~"

if __name__ == "__main__":
    app.run()

