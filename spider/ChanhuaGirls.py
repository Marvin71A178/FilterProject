#彰化女中
import json
import os

load = open("./projects/index.json", 'r' , encoding="utf-8" )
js = json.load(load)
load.close()

for j in js:

    article={
        "source_web_name":j["source_web_name"],
        "source_url": j["source_url"],
        "url" : j["url"],
        "title" : j["title"],
        "content" : j["content"],
        "date":j["date"],
        "image":[j["image"]],
        "id":0
    }

    if not os.path.isfile("./projects/index1.json"): # initailize the json file
            with open("./projects/index1.json", "w") as InitialFile:
                InitialFile.write("[]")
    with open("./projects/index1.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 
    
    jsonDict.append(article)

    with open("./projects/index1.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )


