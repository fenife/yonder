#!/usr/bin/env python3

import json
from starry.application import Application

app = Application()


@app.route('/')
def index(ctx):
    data = {'a': 1, 'b': 2}
    resp = {
        "status": 200,
        "data": data
    }
    resp = json.dumps(resp).encode()
    # resp = b"hello yonder"
    return resp


def _test():
    # app = Application()
    host = '0.0.0.0'
    port = 6070
    app.run(host=host, port=port)


if __name__ == "__main__":
    _test()
