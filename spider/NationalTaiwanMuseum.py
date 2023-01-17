#國立台灣美術館
import requests
from bs4 import BeautifulSoup
import os
import json
import datetime
now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
try:
    
    url_list = []
    title = []
    dates = []

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}


    resource_path = "./projects"

    if not os.path.exists(resource_path):
        os.mkdir(resource_path)



    def date (urls,dates,soup):
        urls = soup.find_all("span",class_ = "date")
        for url in urls:
            dates.append(url.text.replace(" ", "").replace("\r", "").replace("\xa0", "").replace("\n",""))
        

    for i in range(1,3):
        o_url = "https://www.ntmofa.gov.tw/activitysoonlist_1052_{}.html".format(i)

        

        res = requests.get(o_url,headers)
        soup = BeautifulSoup(res.text,"html.parser")

        date(o_url,dates,soup)
        
        urls = soup.find_all("li")
        try:
            for url in urls:
                string = url.a['href']
                if string[:64] == "https://event.culture.tw/NTMOFA/portal/Registration/C0103MAction":
                    url_list.append(url.a['href'])
                    title.append(url.a.text)
        except IndexError as e:
            continue
    url_list.pop()
    title.pop()

    for ur in url_list:
        res_u = requests.get(ur,headers)
        soup_u = BeautifulSoup(res_u.text,"html.parser")
        content_list = []
        
        contents = soup_u.find("div",class_ = "ckEdit html")  
        for content in contents.find_all('p'):
            content_list.append(content.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))
        content_str = ' '.join(content_list)

        image_html = soup_u.find("div",class_ =  "photo_01")
        image = "https://event.culture.tw"+image_html.img['src']

        
        article ={
            "source_web_name":"台灣美術館",
            "source_url":"https://www.ntmofa.gov.tw/",
            "url" : ur,
            "title" : title[url_list.index(ur)],
            "content" : content_str,
            "date" : dates[url_list.index(ur)],
            "image":[image],
            "id" : 0,
        }

        if not os.path.isfile("./projects/index.json"): # initailize the json file
            with open("./projects/index.json", "w") as InitialFile:
                InitialFile.write("[]")

            
        with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 


        jsonDict.append(article) #add all every dic in to this list
            
        with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )
            
                
    record_runtime(f"\nNationalTaiwanMuseum上次更新時間為:{now}\n\t執行成功")
except:
    record_runtime(f"\nNationalTaiwanMuseum上次更新時間為:{now}\n\t**執行失敗")
