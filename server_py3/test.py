#!/usr/bin/env python3

import requests
import time

url = "http://localhost:6070/users/"

for i in range(100):
    r = requests.get(url)
    print(f"{i:02d} {r}")
    time.sleep(0.01)

