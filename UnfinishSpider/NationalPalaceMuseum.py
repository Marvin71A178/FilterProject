# 國立故宮博物館
from bs4 import BeautifulSoup
import requests
import json
import base64
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

request_session = requests.session()

res = request_session.get(
    "https://www.npm.gov.tw/Activity-Current.aspx?sno=03000079&l=1", headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# with open("./test.txt",  "w", encoding="utf-8") as e:
#     e.write(str(soup))
OutputActivities = []
for i in soup.find_all("li", {"class": "mb-8"}):
    dic = {
        "Title": i.find("h3", {"card-title-underline h4"}).text.strip(),
        "Content": "",
        "Sources": ["https://www.npm.gov.tw/"+i.find("a", {"class": "card card-horizontal card-height-sm"})["href"]],
        "Date": i.find("div", {"class": "h5"}).text.strip(),
    }
    if i.find("img"):
        dic["Images"] = ["https://www.npm.gov.tw/" +
                         str(i.find("img")["data-src"])]
    try:
        sub_res = request_session.get(dic["Sources"][0])
        print(dic["Sources"][0])
        sub_soup = BeautifulSoup(sub_res.text, "html.parser")
        dic["html"] = sub_soup.find(
            "div", {"class": "container-article-default"})
        Contents = dic["html"].find_all(text=True)
        dic["Content"] = "\n".join(Content.strip() for Content in Contents)
        dic["html"] = base64.b64encode(
            str(dic["html"]).encode("utf-8")).decode('utf-8')
        OutputActivities.append(dic)
    except Exception as e:
        print(e)
        continue

with open("./FilterTools/SpiderData/NationalPalaceMuseum.json", "w", encoding="utf-8") as writeFile:
    json.dump(OutputActivities, writeFile, ensure_ascii=False, indent=4)
