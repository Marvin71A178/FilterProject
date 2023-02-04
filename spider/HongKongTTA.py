#香港卓藝協會
import requests
from bs4 import BeautifulSoup
import os 
import json
import datetime
now = datetime.datetime.now()


def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
try:

    o_url = "https://tta.hk/"

    titles = []
    urls = []

    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    res = requests.get(o_url,header)
    soup = BeautifulSoup(res.text,"html.parser")

    entrys = soup.find_all("h1",class_ = "elementor-heading-title elementor-size-default")

    for entry in entrys:
        try:
            urls.append(entry.a['href'])
            titles.append(entry.text)
        except TypeError as e:
            continue
    OutputList = []
    for url in urls:

        res_next = requests.get(url,header)
        soup_next = BeautifulSoup(res_next.text,"html.parser")

        im_url = soup_next.find_all("div" , class_ = "elementor-image")[1]

        images = im_url.img['data-srcset'].split(", ")
        image_list = []
        for image in images:
            image_list.append(image.split(" ")[0])

        contents = soup_next.find_all("div",class_ = "elementor-text-editor elementor-clearfix")
        content_list = []


        for content in contents:

            content_list.append(content.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))

            if content.text[0:6] == "比賽獎項 :":
                break
        content_str = ' '.join(content_list)

        article = {
            "Title" : titles[urls.index(url)],
            "Content" : content_str,
            "Sources" : [o_url , url] ,
            "Images": image_list
        }
        OutputList.append(article)
    
    with open("./FilterTools/SpiderData/HongKongTTA.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputList , writeFile, ensure_ascii=False, indent=4)

    record_runtime(f"\nHongKongTTA上次更新時間為:{now}\n\t執行成功")
except Exception as e :
    record_runtime(f"\nHongKongTTA上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
