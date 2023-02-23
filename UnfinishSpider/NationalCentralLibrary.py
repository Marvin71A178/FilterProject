import requests
from bs4 import BeautifulSoup
import json
import base64
import asyncio
import datetime
import aiohttp

now = datetime.datetime.now()


async def fecth(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.text())
            return response.text()


def step1():
    card_li = []
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    url = "https://www.ncl.edu.tw/activityhistorylist_238.html"
    res = requests.get(url, headers=headers)
    # print(res.status_code)
    soup = BeautifulSoup(res.text, "html.parser")

    for i in soup.find_all("div", {"class": "clients-page"}):
        Dateli = [t.text for t in i.find_all("span")]
        date = "~".join(Dateli)
        dic = {
            "Title": i.a["title"],
            "Content": "",
            "Sources": ["https://www.ncl.edu.tw/" + i.a["href"]],
            "Date": date
        }
        card_li.append(dic)
    return card_li


async def main(card):
    print(card["Sources"][0])
    res = await fecth(card["Sources"][0])
    print(res)


async def step2(card_li):
    task = [main(card) for card in card_li]
    await asyncio.gather(*task)

card_li = step1()
asyncio.run(step2(card_li))
# with open("./test.json" . )
