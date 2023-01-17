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

    resource_path = "./projects"

    if not os.path.exists(resource_path):
        os.mkdir(resource_path)



    urls = soup.find_all("div" , class_ = "css_td list_title")
    table = soup.find_all("div",class_ = "css_td list_date")


    for url in urls:
        title.append(url.text.replace("\n",""))
        hrefs.append("https://culture.tycg.gov.tw/"+url.a['href'])

    for tabl in table:
        dates.append(tabl.text)

    content = []

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

        article ={
            "source_web_name":"桃園文化局",
            "source_url":"hhttps://culture.tycg.gov.tw/index.jsp",
            "url" : href,
            "title" : title[hrefs.index(href)],
            "content" : content_str,
            "date" : dates[hrefs.index(href)].replace("-","/"),
            "image":img_list,
            "id" : 0,
        }

    # if os.path.isfile("./projects/index.json"): # initailize the json file
        with open("./projects/index.json", "w") as InitialFile:
            InitialFile.write("[]")

            
        with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 


        jsonDict.append(article) #add all every dic in to this list
            
        with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )

        
            
    record_runtime(f"\nTaoyuanCultureAffairs上次更新時間為:{now}\n\t執行成功")
except:
    record_runtime(f"\nTaoyuanCultureAffairs上次更新時間為:{now}\n\t**執行失敗")
