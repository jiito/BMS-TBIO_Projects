#!/usr/bin/env python3.6

import json

atp_packages = []
r_packages = []


with open("json-dockerfile.json", "r") as f:
    data = json.load(f)

    for i in data["apt"]:
        try:
            name = i["name"]
            version = i["version"]
            print("{}={}".format(i["name"], i["version"]))
        except KeyError as no_version:
            print(name)            