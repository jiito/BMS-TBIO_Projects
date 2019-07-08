#!/usr/bin/env python3.6

import json

with open("json-dockerfile.json", "r") as f:
    data = json.load(f)

    for i in data["apt"]:
        print(i)