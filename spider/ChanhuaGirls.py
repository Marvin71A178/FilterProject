from bs4 import BeautifulSoup
import asyncio
import requests
import json
import time
from selenium import webdriver
import datetime
import base64
import aiohttp
now = datetime.datetime.now()


def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ ChanhuaGirls\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")
finish = 0 

def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)

async def fecth(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            return await res.text()
async def catch_element(url,OutputList,total):
    global finish
    href = url.a['href']
    res = await fecth(href)
    small_soup = BeautifulSoup(res, "html.parser")

    contents = small_soup.find("div", class_="entry-content clr")
    con = []
    for content in contents.find_all('p'):
        con.append(content.text)
    body_str = '\n'.join(con)

    outputdic = {
        "Title": url.a["title"],
        "Content": body_str,
        "Sources": ["https://www.chgsh.chc.edu.tw/tag/game/",href],
        "html": base64.b64encode(str(contents).encode("utf-8")).decode('utf-8')
    }
    finish += 1
    printProgressBar(finish, total)
    if body_str == "":
        return
    OutputList.append(outputdic)
async def main():
        driver = webdriver.Chrome("./Tools/chromedriver.exe")
        url = "https://www.chgsh.chc.edu.tw/tag/game/"
        driver.get(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
        temp_height = 0

        prev_ele = None
        while True:
            driver.execute_script("window.scrollBy(0,1000)")

            check_height = driver.execute_script(
                "return document.      documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")

            if check_height == temp_height:
                break
            temp_height = check_height

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        driver.close()

        blog = soup.find("div", {"id": "blog-entries"})

        element = blog.find_all("h2", {"class": "blog-entry-title entry-title"})
        total = len(element)
        OutputList =[]
        tasks = [catch_element(x,OutputList,total) for x in element]
        await asyncio.gather(*tasks)

        with open("./FilterTools/SpiderData/ChanhuaGirls.json", "w", encoding="utf-8") as writeFile:
            json.dump(OutputList, writeFile, ensure_ascii=False, indent=4)

asyncio.run(main())