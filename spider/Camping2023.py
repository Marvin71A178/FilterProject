# 大學營隊
from bs4 import BeautifulSoup
import requests
import json
import copy
import datetime
import base64
now = datetime.datetime.now()
def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ Camping2023\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")

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
    html = []
    OriActivity = {"Title": "",
                "Content": "",
                "Images": [],
                "Sources": ["https://students.tw/5599/"],
                "html": []
                }
    Activity = copy.deepcopy(OriActivity)
    total_post = len(list(OriActivities.children))
    finished_post = 0
    for child in OriActivities.children:
        finished_post += 1
        printProgressBar(finished_post, total_post)
        if child == "\n":
            continue
        elif child.name == "h3":
            if firstActivity:
                firstActivity = False
                Activity = copy.deepcopy(OriActivity)
                Activity["Title"] = child.text
                html = []
                continue
            else:
                html_tem = []
                for html_code in Activity["html"]:
                    html_tem.append(str(html_code))

                    texts = html_code.find_all(text=True)
                    text = "\n".join(Content.strip() for Content in texts)
                    Activity["Content"] = Activity["Content"] + text + "\n"

                html_tem = "".join(html_tem)
                # Activity["html"] = html_tem
                Activity["html"] = html_tem.encode("utf-8")
                Activity["html"] = base64.b64encode(Activity["html"]).decode('utf-8')
                # Activity["html"] = ''.join(
                #     r'\u{:04X}'.format(ord(chr)) for chr in html_tem)

                Activities.append(Activity)
                html = []
                Activity = copy.deepcopy(OriActivity)
                Activity["Title"] = child.text
                continue

        elif child.name == "figure":
            # texts = child.find_all(text=True)
            # text = "\n".join(text.strip() for text in texts)
            # Activity["Content"] = Activity["Content"] + text + "\n"
            html.append(child)
            selectImgs = child.select("picture > img")
            for i in selectImgs:
                Activity["Images"].append(i.attrs["src"])
        else:
            # texts = child.find_all(text=True)
            # text = "\n".join(text.strip() for text in texts)
            # Activity["Content"] = Activity["Content"] + text + "\n"
            html.append(child)
        Activity["html"] = html
        
    with open("./FilterTools/SpiderData/Camping2023.json", "w", encoding='utf-8') as writeFile:
        json.dump(Activities, writeFile, ensure_ascii=False, indent=4)


    record_runtime(f"\nCamping2023上次更新時間為:{now}\n\t執行成功")
except Exception as e :
    record_runtime(f"\nCamping2023上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
    print(e)
