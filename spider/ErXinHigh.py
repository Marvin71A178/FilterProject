#私立二信高級中學
import requests
from bs4 import BeautifulSoup
import os
import json
from requests.adapters import HTTPAdapter
import datetime
now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
        
        
        
def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")
try:

    header  = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    hrefs = []
    titles = []

    for page in range(1,29):
        s =requests.session()
        s.mount("https://", HTTPAdapter(max_retries=3))
        o_url = "https://esshb.essh.kl.edu.tw/%e5%a4%9a%e5%85%83%e5%ad%b8%e7%bf%92%e8%b3%87%e8%a8%8a%e7%ab%99/?lcp_page0={}#lcp_instance_0".format(page)

        
        res = s.request("GET",o_url,header,timeout=3)
        soup = BeautifulSoup(res.text,"html.parser")

        urls = soup.find("ul" , class_ = "lcp_catlist")

        for url in urls.find_all("li"):

            hrefs.append(url.a['href'])

            titles.append(url.a.text)
    OutputActivity = []
    finished_post = 0
    total_post = len(hrefs)
    for href in hrefs :
        s = requests.session()
        s.mount("https://", HTTPAdapter(max_retries=5))
        res_in = s.request("GET", href,header,timeout=4)
        
        soup_in = BeautifulSoup(res_in.text,"html.parser")

        contents = soup_in.find("div",class_ = "entry-content").text.replace(" ", "").replace("\r", "").replace("\xa0", "")

        img_list = []
        
        try:
            img = soup_in.find("img",decoding = "async")
            img_urls = img['srcset'].split(", ")
            
            for img_url in img_urls:
                if img_url !="https://secure.gravatar.com/avatar/924de1f0c4efd8d506e8508826a3cf45?s=98&d=mm&r=g":
                    img_list.append(img_url.split(" ")[0])
        except TypeError as e:
            continue
        
    
        if img_list != [] or img_list == ["https://secure.gravatar.com/avatar/924de1f0c4efd8d506e8508826a3cf45?s=98&d=mm&r=g"]:
            article = {
                "Title" : titles[hrefs.index(href)],
                "Content" : contents,
                "Sources" : ["https://esshb.essh.kl.edu.tw/" , href] ,
                "Images":img_list,
            }
        else:
            article = {
                "Title" : titles[hrefs.index(href)],
                "Content" : contents,
                "Sources" : ["https://esshb.essh.kl.edu.tw/" , href]
            }

        
        OutputActivity.append(article) #add all every dic in to this list
        finished_post += 1
        printProgressBar(finished_post, total_post)
    with open("./FilterTools/SpiderData/ErXinHigh.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputActivity , writeFile, ensure_ascii=False, indent=4)
    record_runtime(f"\nErXinHigh上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nErXinHigh上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")

