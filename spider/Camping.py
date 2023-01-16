#大學營隊
from bs4 import BeautifulSoup
import requests 
import os
import json
import re
import uuid
import datetime
now = datetime.datetime.now()
date_t = "上次更新時間為: " + str(now) 
with open("C:\\Users\\aazz1\\OneDrive\\桌面\\store_code\\Filter\\re_filter_tool\\daily_crawler\\camping\\test.txt" , "w", encoding="utf-8") as writefile:
    writefile.write(date_t)
url = "https://students.tw/5599/"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C hrome/105.0.0.0 Safari/537.36"}

res = requests.get(url , headers = headers)
soup = BeautifulSoup(res.text,"html.parser")

title = soup.find_all("h3",class_="ftwp-heading")
content = soup.find_all("p")

image = soup.find_all("figure", class_ = "wp-block-image size-full")


resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)


list1 = []
rstr  =  r"[\/\\\:\*\?\"\<\>\|]" 

for tit in title:#營隊標題
    con = str(tit.text).replace(" ", "").replace("\r", "").replace("\n", "").replace("\xa0", "")
    con = re.sub(rstr,"",con)
    list1.append(con)


#p's content
p_list = []
for p in content:
    
    p_list.append(p.text)



image = []
for tit in title:
    try:
        images = tit.find_next_sibling("figure")
        image.append(images.source['srcset'])
    except TypeError as e:
        image.append("")
    




text = {}

p_list = p_list[25:3244]

#method handle the url
def urls(res,list):
    
    title = soup.find_all("p")
    times = 0

    for i in title:
        try:
            if str(i.text) =="➤額外補充的資訊：報名表單":
                url_list.append(i.a['href'])        
            elif str(i.text) == "➤粉專網址：點擊前往":
                url_list.append(i.a['href'])
            elif str(i.text) == "➤報名網址：點擊前往":
                url_list.append(i.a['href'])
            elif str(i.text) == "➤詳細資訊：點擊前往":
                url_list.append(i.a['href'])
            elif str(i.text) == "➤官方網站：點擊前往":
                url_list.append(i.a['href'])    
            elif str(i.text) == "➤粉專網址：https://www.facebook.com/events/5357289340952836/?ref=newsfeed":
                string = i.text
                chan = string.split("：")
                url_list.append(chan[1])
            elif str(i.text) == "➤更多營隊資訊＆報名連結：點擊前往":
                url_list.append(i.a['href'])
            elif str(i.text) == "➤營隊詳細資訊與報名連結：點擊前往":
                url_list.append(i.a['href'])
            
            elif str(i.strong.a.text) == "點擊前往":
                url_list.append(i.a['href'])    

        except AttributeError as e:
            continue
        except TypeError as e1:
            continue
    url_list.remove("https://forms.gle/wFQzPLKDHaGGVE4w7")

#method to process the date
def save_date(ary):
    for i in content:
        if str(i.text)[:5] =="➤活動日期":
            ary.append(str(i.text)[6:])
    ary[17]="2"+ary[17]


#list to save urls
url_list = []
urls(res,url_list)


#list to save date
date = []
save_date(date)


#method to handle the content
content = []
cont = "" 
j=0
for titles in range(0,len(list1)):
    
    for i in range(j,3219):
        try:
            if p_list[i+1]=="➤主辦單位：啟夢教育":
                cont+=p_list[i]
                j=i+1
                break
            elif p_list[i+1][3]!="名":
                cont+=p_list[i]+"\n"
            elif p_list[i+1][3]=="名":
                cont+=p_list[i]
                j=i+1
                break
           
        except IndexError as e:
            cont+=p_list[i]+"\n"
    content.append(cont)

    cont = ""

# To save the content in json
for allthings in range(0,len(list1)):
    article={
        "source_web_name":"【2023寒假大學營隊】精選全臺370+營隊報名資訊",
        "source_url": url,
        "url" : url_list[allthings],
        "title" : list1[allthings],
        "content" : content[allthings],
        "date":date[allthings],
        "image":image[allthings],
        "id":0
    }
    if not os.path.isfile("./projects/index.json"): # initailize the json file
            with open("./projects/index.json", "w") as InitialFile:
                InitialFile.write("[]")
    with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 
    
    jsonDict.append(article)

    with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )









