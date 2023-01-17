# 大學營隊
from bs4 import BeautifulSoup
import requests
import json
import copy
import datetime
now = datetime.datetime.now()


def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)


try:
    url = "https://students.tw/5599/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C hrome/105.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=header)
    if res.status_code == 404:
        record_runtime(f"\nCamping2023上次更新時間為:{now}\n\t**執行失敗 404Error")
    soup = BeautifulSoup(res.text, "html.parser")
    OriActivities = soup.select_one("#ftwp-postcontent")

    Activities = []
    firstActivity = True
    OriActivity = {"Title": "",
                   "Content": "",
                   "Images": [],
                   "Sources": ["https://students.tw/5599/"]
                   }
    for child in OriActivities.children:
        if child == "\n":
            continue
        elif child.name == "h3":
            if firstActivity:
                firstActivity = False
                Activity = copy.deepcopy(OriActivity)
                Activity["Title"] = child.text
                continue
            else:
                Activities.append(Activity)
                Activity = copy.deepcopy(OriActivity)
                Activity["Title"] = child.text
                continue

        elif child.name == "p":
            texts = child.find_all(text=True)
            text = "\n".join(text.strip() for text in texts)
            Activity["Content"] = Activity["Content"] + text + "\n"

        elif child.name == "figure":
            texts = child.find_all(text=True)
            text = "\n".join(text.strip() for text in texts)

            Activity["Content"] = Activity["Content"] + text + "\n"
            selectImgs = child.select("picture > img")
            for i in selectImgs:
                Activity["Images"].append(i.attrs["src"])
    with open("./FilterTools/SpiderData/Camping2023.json", "w", encoding="utf-8") as writeFile:
        json.dump(Activities, writeFile, ensure_ascii=False, indent=4)

    record_runtime(f"\nCamping2023上次更新時間為:{now}\n\t執行成功")
except:
    record_runtime(f"\nCamping2023上次更新時間為:{now}\n\t**執行失敗")
