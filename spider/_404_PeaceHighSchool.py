#和平高中
from bs4 import BeautifulSoup
import requests
import os
import json
import time

url = "http://www.hpsh.tp.edu.tw/news/u_news_v1.asp?id=%7BB821C671-C9EA-44BC-A7C4-0C8774DC58EE%7D&fid=47"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

res = requests.get(url,headers = headers)
print("ok" if res.ok else "connection failed")
res.encoding='utf-8'

soup = BeautifulSoup(res.text,"html.parser")

titles= soup.find_all("td",align = "left")

resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)

url_list = []
url_title = []
url_content = []

#to get the title and url to enter the next web
for title in titles :
    string = title.text
    
    if(string[0:4] !="【推廣】"):
        url_title.append(string)
        url_list.append("http://www.hpsh.tp.edu.tw/news/"+title.a['href'])
    else:
        continue

for title in url_list:
    url_res = requests.get(url = title,headers =headers)
    url_res.encoding = "utf-8"
    url_soup = BeautifulSoup(url_res.text, "html.parser")
                                                                 
    sm_url = url_soup.find_all("td", class_="C-tableA3")

    contents = []

    content = ""
    for urls in sm_url[4]:
        contents.append(urls.text)
    # print(contents)
    # print(len(contents))
    for content in contents:
        content += "\n"
    url_content.append(content)
    

# for i in range(0,197):
#     print(url_content[i])
#     print("==={}===".format(i))

print("載入完成 即將轉成JSON格式")




all = len(url_content)

for i in range(0,197):
    article = {
        "sourse_web_name":"國立和平高中",
        "source_url":url,
        "url" : None,
        "title" : url_title[i],
        "content" : url_content[i],
        "date" : None,
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