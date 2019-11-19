#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)


@app.route('/<string:name>')
def hello_world(name):
    return f"Hello {name}!"


if __name__ == '__main__':
    app.run()
