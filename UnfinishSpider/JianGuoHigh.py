#建國高級中學
#page update
import requests
from bs4 import BeautifulSoup
import os 
import json
import datetime
now = datetime.datetime.now()
def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ JianGuoHigh\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")

def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
try:
    titles = []
    hrefs = []
    header  = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    for i in range(1,7):
        o_url = "https://www2.ck.tp.edu.tw/news/category/3?page={}".format(i)

        
        res = requests.get(o_url,header)
        soup = BeautifulSoup(res.text,"html.parser")

        find_hrefs = soup.find_all("div","List__ListItemWrapper-sc-1li2krx-9 ceDUDg")

        for find_href in find_hrefs:
            if find_href.a['title'][2:10]  !="國立陽明交通大學":
                hrefs.append("https://www2.ck.tp.edu.tw"+find_href.a['href'])
                titles.append(find_href.a['title'])
    OutputActivity = []
    for href in hrefs:
        
        res_in = requests.get(href)
        
        soup_in = BeautifulSoup(res_in.text,"html.parser")
        contents = soup_in.find("div","Page__RedactorBlock-sc-1geffe8-0 redactor-styles hkzaDk")
        content_list = []
        for content in contents.find_all("p"):
            content_list.append(content.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))
        content_str = ' '.join(content_list)
        
        related_url = []
        try:
            files = soup_in.find("div","Post__LinkWrapper-kr2236-3 iaPBqD")
            for file in files.find_all("a"):
                related_url.append(file['href'])
        except AttributeError as e:
            related_url = []
        if related_url != []:
            article = {
                "Title": titles[hrefs.index(href)],
                "Content" :content_str,
                "Sources" :["https://www2.ck.tp.edu.tw/"] + related_url
            }
        else:
            article = {
                "Title": titles[hrefs.index(href)],
                "Content" :content_str,
                "Sources" :["https://www2.ck.tp.edu.tw/"] 
            }
        OutputActivity.append(article)
        
    with open("./FilterTools/SpiderData/JianGuoHigh.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputActivity , writeFile, ensure_ascii=False, indent=4)
                        
    record_runtime(f"\nJianGuoHigh上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nJianGuoHigh上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")

