import json

filename = "TEMP.json"


with open(filename, "r", encoding="utf-8") as jsonFile:
    post_list = json.load(jsonFile)
