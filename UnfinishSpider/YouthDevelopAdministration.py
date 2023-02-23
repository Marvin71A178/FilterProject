#青年發展署
import requests
from bs4 import BeautifulSoup
import numpy as np
import datetime
import itertools
import json
now = datetime.datetime.now()
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
class Activity():
    def __init__(self,url,image):
        self.url = url
        
        self.Content = ""
        self.Images = [image]
        self.Sources = ""
        res = requests.get(self.url , headers = headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.Title = soup.find("h2", {"class" : "page-title"}).text.strip()
        cont = soup.find("div", {"class" : "cont"} ).find_all(text = True)
        self.Content = "\n".join(Content.strip() for Content in cont)
        
    def OutputFormat(self):
        Format = {
            "Title" : self.Title,
            "Content" : self.Content,
            "Images" : self.Images,
            "Sources" : [self.url]
        }
        return Format

def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
try:
    Activities_dic = {}
    Activities_dic_len = 0
    for i in itertools.count(start= 1):
        
        o_url = f"https://www.yda.gov.tw/EventList.aspx?uid=101&pid=56&page={i}"
        res = requests.get(o_url, headers = headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        linkList = soup.find_all("div",{"class" : "event-box"})
        for j in linkList:
            Links = j.find_all("a")
            for Link in Links:
                for child in Link.children:
                    if child.name == "figure":
                        image = Link.find("img")
                        Activities_dic["https://www.yda.gov.tw/" + Link["href"]] = "https://www.yda.gov.tw" + image["src"]
        if len(Activities_dic) == Activities_dic_len:
            break
        else:
            Activities_dic_len = len(Activities_dic)
    OutputAvtivity = []
    for key, value in Activities_dic.items():
        obj = Activity(key,value)
        OutputAvtivity.append(obj.OutputFormat())
    
    with open("./FilterTools/SpiderData/YouthDevelopAdministration.json", "w",  encoding="utf-8") as writeFile:
        json.dump(OutputAvtivity, writeFile, ensure_ascii=False, indent=4)
    record_runtime(f"\nYouthDevelopAdministration上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nYouthDevelopAdministration上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")