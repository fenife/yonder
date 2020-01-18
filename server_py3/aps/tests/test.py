#!/usr/bin/env python3

import requests
import time


def performance():
    url = "http://localhost:6070/users/"

    for i in range(100):
        r = requests.get(url)
        print(f"{i:02d} {r}")
        time.sleep(0.01)


class A(object):
    code = 'a'

    def __init__(self, code=None):
        if code is not None:
            self.code = code


def test():
    a = A(code=1)
    b = A()
    print(a.code)
    print(b.code)


if __name__ == '__main__':
    # performance()
    test()
