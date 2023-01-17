# 彰化女中
import json
import os
import datetime
now = datetime.datetime.now()


def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)


try:
    load = open("./projects/index.json", 'r', encoding="utf-8")
    js = json.load(load)
    load.close()

    for j in js:

        article = {
            "source_web_name": j["source_web_name"],
            "source_url": j["source_url"],
            "url": j["url"],
            "title": j["title"],
            "content": j["content"],
            "date": j["date"],
            "image": [j["image"]],
            "id": 0
        }

        if not os.path.isfile("./projects/index1.json"):  # initailize the json file
            with open("./projects/index1.json", "w") as InitialFile:
                InitialFile.write("[]")
        # transfer the article dic to json
        with open("./projects/index1.json", "r", encoding="utf-8") as JsonFile:
            jsonDict = json.load(JsonFile)

        jsonDict.append(article)

        # write this to the json file
        with open("./projects/index1.json", "w",  encoding="utf-8") as writeFile:
            json.dump(jsonDict, writeFile, ensure_ascii=False, indent=1)

    record_runtime(f"\nChanhuaGirls上次更新時間為:{now}\n\t執行成功")
except:
    record_runtime(f"\nChanhuaGirls上次更新時間為:{now}\n\t**執行失敗")
