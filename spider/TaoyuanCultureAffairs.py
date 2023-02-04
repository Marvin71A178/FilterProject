#桃園市政府文化局
import requests
from bs4 import BeautifulSoup
import json 
import os
import datetime
now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
try:
    o_url = "https://culture.tycg.gov.tw/home.jsp?id=93&parentpath=0,16"

    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    res = requests.get(o_url,header)
    soup = BeautifulSoup(res.text,"html.parser")

    title = []
    hrefs = []
    dates = []

    urls = soup.find_all("div" , class_ = "css_td list_title")
    table = soup.find_all("div",class_ = "css_td list_date")


    for url in urls:
        title.append(url.text.replace("\n",""))
        hrefs.append("https://culture.tycg.gov.tw/"+url.a['href'])

    for tabl in table:
        dates.append(tabl.text)

    content = []
    OutputActivity = []
    for href in hrefs:

        h_res = requests.get(href,header)
        h_soup = BeautifulSoup(h_res.text,"html.parser")
        content_list = []
        img_list = []
        contents = h_soup.find_all("div",class_ = "content_detail_row")

        images = h_soup.find_all("div",class_ = "div_pic")
        for image in images:
            img_list.append("https://culture.tycg.gov.tw/"+image.a['href'][1:])

        for content in contents:
            content_list.append(content.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))
        content_str = ' '.join(content_list)
        if img_list == []:
            img_list = None
        article ={
            "Title" :title[hrefs.index(href)],
            "Content" :content_str,
            "Sources" : ["https://culture.tycg.gov.tw/" , href],
            "Date" : dates[hrefs.index(href)].replace("-","/"),
            "Images" :img_list,
        }
        OutputActivity.append(article)
        
    with open("./FilterTools/SpiderData/TaoyuanCultureAffairs.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputActivity , writeFile, ensure_ascii=False, indent=4)

    record_runtime(f"\nTaoyuanCultureAffairs上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nTaoyuanCultureAffairs上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
