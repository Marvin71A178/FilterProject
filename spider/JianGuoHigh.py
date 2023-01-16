#建國高級中學
import requests
from bs4 import BeautifulSoup
import os 
import json

titles = []
hrefs = []
header  = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}


resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)

for i in range(1,7):
    o_url = "https://www2.ck.tp.edu.tw/news/category/3?page={}".format(i)

    
    res = requests.get(o_url,header)
    soup = BeautifulSoup(res.text,"html.parser")

    find_hrefs = soup.find_all("div","List__ListItemWrapper-sc-1li2krx-9 ceDUDg")

    for find_href in find_hrefs:
        if find_href.a['title'][2:10]  !="國立陽明交通大學":
            hrefs.append("https://www2.ck.tp.edu.tw"+find_href.a['href'])
            titles.append(find_href.a['title'])

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
            "source_web_name":"國立建國高級中學",
            "source_url":"https://www2.ck.tp.edu.tw/",
            "url" : related_url,
            "title" : titles[hrefs.index(href)],
            "content" : content_str,
            "date" : None,
            "image":None,
            "id" : 0,
        }
    else:
        article = {
            "source_web_name":"國立建國高級中學",
            "source_url":"https://www2.ck.tp.edu.tw/",
            "url" : None,
            "title" : titles[hrefs.index(href)],
            "content" : content_str,
            "date" : None,
            "image":None,
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


