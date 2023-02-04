# 嘉義文化創意產業園區
import requests
from bs4 import BeautifulSoup
import itertools
import json
import datetime
now = datetime.datetime.now()


def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)


try:
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    allActivity_set = set()
    for i in itertools.count(start=1):
        o_url = f"https://www.g9cip.com/category/activity/page/{i}/"
        res = requests.get(o_url, headers=header)
        soup = BeautifulSoup(res.text, 'html.parser')
        for link in soup.select('article > div > div > div > section > div > div > div > div > div > div > a:not([rel])'):
            allActivity_set.add(link['href'])
        if res.status_code == 404:
            break
    
    ActivityList = []
    for url in allActivity_set:
        
        sub_url = url
        sub_res = requests.get(sub_url, headers=header)
        sub_soup = BeautifulSoup(sub_res.text, "html.parser")
        test_li = sub_soup.find_all(
            "div", class_=["elementor-heading-title", "elementor-size-default"])
        title_li = []
        content_li = []
        mainBody = sub_soup.select(
            "body > div > section > div > div > div > section > div > div")
        img_url = []
        Content = ""
        for fimg in mainBody:
            if fimg.get("data-settings") == '{"background_background":"classic","_ob_bbad_is_stalker":"no","_ob_teleporter_use":false,"_ob_column_hoveranimator":"no","_ob_column_has_pseudo":"no"}':
                imgli = fimg.select("img")
                #find all content
                Contents = fimg.find_all(text=True)
                Content = "\n".join(Content.strip() for Content in Contents)
                for k in imgli:
                    img_url.append(k["data-src"])
        for i in test_li:
            if i.find("a") == None:
                title_li.append(i.text)
            content_li.append(i.text)
        title = title_li[4]
        holder = ""
        for i in range(len(content_li)):
            if content_li[i] == "主辦單位":
                holder = content_li[i+1]
                break

        date = ""
        for i in range(len(content_li)):
            if content_li[i] == "日期":
                date = content_li[i+1]
                break

        site = ""
        for i in range(len(content_li)):
            if content_li[i] == "地點":
                site = content_li[i+1]
                break
        
        
        Activity_dic = {
            
            "Title": title,
            "Date": date,
            "Content": Content,
            "Location": site,
            "Holder": holder,
            "Images": img_url,
            "Sources": ["https://www.g9cip.com/",url]
        }

        ActivityList.append(Activity_dic)

    with open("./FilterTools/SpiderData/G9CreativeParkCrawler.json", "w",  encoding="utf-8") as writeFile:
        json.dump(ActivityList, writeFile, ensure_ascii=False, indent=4)

    record_runtime(f"\nG9CreativeParkCrawler上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nG9CreativeParkCrawler上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
