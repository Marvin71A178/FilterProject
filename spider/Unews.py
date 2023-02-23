import requests
from bs4 import BeautifulSoup
import base64
import itertools
import datetime
import json
import asyncio
import aiohttp

def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ Unews\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


async def fecth(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print(url)
            return await res.text()


async def step1():
    pages = dict()
    task = [fecth(
        f"https://www.unews.com.tw/News/Active?type=0&cur={i}") for i in range(1, 100)]
    fecthReturn = await asyncio.gather(*task)
    for page in fecthReturn:
        soup = BeautifulSoup(page, "html.parser")
        for act in soup.find_all("figure", {"class": "col-xs-12 col-sm-6"}):

            href = "https://www.unews.com.tw" + act.find("a")["href"]
            if pages.get(href, False):
                return pages
            else:
                pages[href] = [
                    act.find("span", {"class": "title"}).text, "https://www.unews.com.tw" + act.find("img")["src"]]
                print(pages[href])


async def fetch(key, OutputActivity, pages):
    print(key)
    async with aiohttp.ClientSession() as session:
        async with session.get(key) as response:
            
            res = await response.text()

            soup = BeautifulSoup(res, "html.parser")

            html = soup.find("div" , {"class" : "page_content"}).find("div" ,{"class" : "col-xs-12"})
            Contents = html.find_all(text=True)
            Content = "\n".join(Content.strip() for Content in Contents)

            dic = {
                "Title": pages[key][0],
                "Content": Content,
                "Sources": [key],
                "Images": [pages[key][1]],
                "html": base64.b64encode(str(html).encode("utf-8")).decode('utf-8')
            }
            OutputActivity.append(dic)
            

Output = asyncio.run(step1())
with open("./test.json", "w", encoding="utf-8") as writeFile:
    json.dump(Output, writeFile, ensure_ascii=False, indent=4)


async def main(OutputActivity, pages):

    task = []
    for key, value in pages.items():
        task.append(fetch(key, OutputActivity, pages))
    await asyncio.gather(*task)
OutputActivity = []
asyncio.run(main(OutputActivity, Output))
with open("./test.json", "w", encoding="utf-8") as writeFile:
    json.dump(OutputActivity, writeFile, ensure_ascii=False, indent=4)
