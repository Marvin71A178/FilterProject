# 賞金獵人
import requests
from bs4 import BeautifulSoup
import numpy as np
import datetime
import itertools
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.service import Service


def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ Hunter\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")


now = datetime.datetime.now()

try:
    def record_runtime(text):
        with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
            writefile.write(text)
    r = requests.get(
            f"https://api.bhuntr.com/cms/bhuntr/contest?language=tw&target=competition&limit=18&page=1&sort=mixed&keyword=&timeline=notEnded&identify=&prizeRange=none&location=none&deadline=none&category=&canApplyCertificate=no")
    test = json.loads(r.content.decode("utf-8"))
    totalpage = test["payload"]["page"]["last"]
    OutputActivity = []
    finished_post = 0
    for i in range(1, totalpage+1):
        finished_post += 1
        printProgressBar(finished_post, totalpage)
        r = requests.get(
            f"https://api.bhuntr.com/cms/bhuntr/contest?language=tw&target=competition&limit=18&page={i}&sort=mixed&keyword=&timeline=notEnded&identify=&prizeRange=none&location=none&deadline=none&category=&canApplyCertificate=no")
        test = json.loads(r.content.decode("utf-8"))
        for j in test["payload"]["list"]:
            html = j["guideline"]
            soup = BeautifulSoup(html, "html.parser")
            Contents = soup.find_all(text=True)
            Content = "\n".join(Contents)
            Title = j["title"]
            Images = [j["coverImage"]["url"]]
            page_url = j["alias"]
            dic = {
                "Title": Title,
                "Content": Content,
                "html": base64.b64encode(str(soup).encode("utf-8")).decode('utf-8'),
                "Images": Images,
                "Sources": ["https://bhuntr.com/tw",
                            "https://bhuntr.com/tw/competitions/" + page_url]
            }
            if j["officialUrl"] != None:
                dic["Sources"].append(j["officialUrl"])
            OutputActivity.append(dic)
        # with open("./test.json", "w", encoding="utf-8") as writeFile:
        #     json.dump(test, writeFile, ensure_ascii=False, indent=4)
    with open("./FilterTools/SpiderData/Hunter.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputActivity, writeFile, ensure_ascii=False, indent=4)

    record_runtime(f"\nHunter上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nHunter上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
