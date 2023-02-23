import requests
from bs4 import BeautifulSoup
import json
import base64
import asyncio
import re
import datetime
import aiohttp

try: 
    nowtime = datetime.datetime.now()
    page_Content = []
    result_Content = []
    max = 0
    now = 0

    def record_runtime(text):
        with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
            writefile.write(text)
    def printProgressBar(now, total, length=20):
        progress = now/total
        progressValue = int((progress)*length)
        print("__ Accupass\r[%s%s] %d/%d" % (
            progressValue * "=",
            (length - progressValue) * " ",
            now,
            total
        ), end="")


    async def fetch(url, max):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                global page_Content
                page_Content.append(await response.text())
                printProgressBar(len(page_Content), max)


    async def actCard(html):
        global max, now, result_Content
        
        soup = BeautifulSoup(html, "html.parser")
        find_event = soup.find_all("div", attrs={'event-row': True})
        l = len(find_event)
        max += l
        
        for act in find_event:

            test = json.loads(act["event-row"])
            dic = {
                "Title": test["name"],
                "Content": "",
                "html": "",
                "Images": [test["photoUrl"]],
                "Sources": ["https://www.accupass.com/event/" + test["eventIdNumber"]],
                "Date": test["fullDateTimeStr"]
            }

            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.accupass.com/v3/events/" + test["eventIdNumber"]) as resp:
                    # print(resp.status)
                    res = await resp.text()
                    de_res = json.loads(res)
                    html = BeautifulSoup(de_res["content"], "html.parser")
                    dic["html"] = base64.b64encode(
                        str(html).encode("utf-8")).decode('utf-8')
                    Contents = html.find_all(text=True)
                    Content = "\n".join(Content.strip() for Content in Contents)
                    dic["Content"] = Content
                    now += 1
                    printProgressBar(now, max)
                    if dic["Content"] == "":
                        return

                    result_Content.append(dic)
                    

    async def step1(MAX_PAGE_CODE):
        tasks = [fetch(
            f"https://old.accupass.com/search/changeconditions/r/0/0/0/0/4/{num}/00010101/99991231", MAX_PAGE_CODE) for num in range(MAX_PAGE_CODE)]
        await asyncio.gather(*tasks)


    async def step2():
        sub_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(sub_loop)
        tasks = [actCard(page) for page in page_Content]
        await asyncio.gather(*tasks)

        with open("./FilterTools/SpiderData/Accupass.json", "w", encoding="utf-8") as writeFile:
            json.dump(result_Content, writeFile, ensure_ascii=False, indent=4)

    now = datetime.datetime.now()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    # GET max page code
    res = requests.get(
        "https://old.accupass.com/search/changeconditions/r/0/0/0/0/4/0/00010101/99991231", headers=headers)
    decode_r = res.content.decode("utf-8")
    soup = BeautifulSoup(decode_r, "html.parser")
    finalPage = soup.find_all("li", {"class": ""}).pop()
    ng_click = finalPage.a.attrs["ng-click"]
    matched = re.search(r"CurrentIndex\":([0-9]+)", ng_click)
    if matched == None:
        print("抓取 MAX page code 失敗")
        exit()

    MAX_PAGE_CODE = int(matched.group(1))
    max = MAX_PAGE_CODE
    now = MAX_PAGE_CODE

    asyncio.run(step1(MAX_PAGE_CODE))
    asyncio.run(step2())
        
    

    record_runtime(f"\nCamping2023上次更新時間為:{nowtime}\n\t執行成功")
except Exception as e :
    record_runtime(f"\nCamping2023上次更新時間為:{nowtime}\n\t**執行失敗\n\t\t{e}")
    print(e)
