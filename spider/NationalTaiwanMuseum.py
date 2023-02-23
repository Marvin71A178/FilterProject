# 國立台灣美術館
# page update
import requests
from bs4 import BeautifulSoup
import os
import json
import datetime
import itertools
import base64
now = datetime.datetime.now()
def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ Hunter\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")

def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)


try:

    url_list = []
    title = []
    dates = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    def date(urls, dates, soup):
        urls = soup.find_all("span", class_="date")
        for url in urls:
            dates.append(url.text.replace(" ", "").replace(
                "\r", "").replace("\xa0", "").replace("\n", ""))

    for i in itertools.count(start=1):

        o_url = "https://www.ntmofa.gov.tw/activitysoonlist_1052_{}.html".format(
            i)
        res = requests.get(o_url, headers)
        soup = BeautifulSoup(res.text, "html.parser")

        date(o_url, dates, soup)
        if not soup.find("div", {"class": "h3"}):
            break
        
        urls = soup.find_all("li")
        try:
            for url in urls:
                string = url.a['href']
                if string[:64] == "https://event.culture.tw/NTMOFA/portal/Registration/C0103MAction":
                    url_list.append(url.a['href'])
                    title.append(url.a.text)
        except IndexError as e:
            continue
        break
    url_list.pop()
    title.pop()
    OutputActivity = []
    for ur in url_list:
        res_u = requests.get(ur, headers)
        soup_u = BeautifulSoup(res_u.text, "html.parser")
        content_list = []

        contents = soup_u.find("div", class_="ckEdit html")
        Contents = contents.find_all(text=True)
        Content = "\n".join(Contents)
        image_html = soup_u.find("div", class_="photo_01")
        image = "https://event.culture.tw"+image_html.img['src']

        article = {
            "Title": title[url_list.index(ur)].strip(),
            "Content": Content,
            "Sources": ["https://www.ntmofa.gov.tw/", ur],
            "html" : base64.b64encode(str(soup).encode("utf-8")).decode('utf-8'),
            "Date": dates[url_list.index(ur)],
            "Images": [image]
        }
        
        OutputActivity.append(article)
    with open("./FilterTools/SpiderData/NationalTaiwanMuseum.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputActivity, writeFile, ensure_ascii=False, indent=4)

    record_runtime(f"\nNationalTaiwanMuseum上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nNationalTaiwanMuseum上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
