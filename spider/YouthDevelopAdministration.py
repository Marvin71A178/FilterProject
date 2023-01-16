#青年發展署
import requests
from bs4 import BeautifulSoup
import os
import uuid
import json
import numpy as np
url = "https://www.yda.gov.tw/"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

res = requests.get(url , headers=headers)
soup = BeautifulSoup(res.text,"html.parser")

##############################################################################################################

title = soup.select('div[class = "regist-btn"]') #the all article's url


img_list = []
img = soup.find_all("figure" , class_ = "img")
for i in img:
    img_list.append("https://www.yda.gov.tw"+i.img['src'])


checker = [] 
def check_url(title):
    for art in title:
        con = str(art.a['href'])
        checker.append(con)

dates = soup.select('small[class = "date"]') 

date_list = []
def date_time(dates):
    for date in dates:
        string = date.text.replace(" ", "").replace("\r", "").replace("\n", " ")
        if string[0:3] ==" 活動":
            date_list.append(string)

date_time(dates)
check_url(title)




resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)

jsonDict = []


#method for getting the JSON file
def get_url(checker):
    i = 0
    for con in checker:
        url_content = "https://www.yda.gov.tw/"+con
        res_content = requests.get(url = url_content,headers = headers)
        soup_content = BeautifulSoup(res_content.text,"html.parser")
        con_title = soup_content.find('h2',class_ = "page-title").text.replace(" ", "").replace("\r", "").replace("\n", " ")
        p_list = []
        body = soup_content.find('div', class_ = "event-info-wrap")

        for p in body.find_all('p'):
            p_list.append(p.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))
        body_str = ' '.join(p_list)

        article = {           #build a dic for one article
            "source_web_name":"青年發展署",
            "source_url":url,
            "url" : url_content,
            "title" : con_title,
            "content" : body_str,
            "date" : date_list[i],
            "image":img_list[i],
            "id" : 0,
        }
        i+=1

        if not os.path.isfile("./projects/index.json"): # initailize the json file
            with open("./projects/index.json", "w") as InitialFile:
                InitialFile.write("[]")

        
        with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 


        jsonDict.append(article) #add all every dic in to this list
        
        with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )
get_url(checker)

#   get_url(checker)
#method to deal with JSON and cut the words to arrange the article
# def cut_article():
#     with open('./projects/index.json',"r",encoding = "utf-8") as readFile:
#         data = json.load(readFile)

#     for content in data :
#         atrticle = content['content']
#         after = "|".join(jieba.cut(atrticle,cut_all=False,HMM=True))
#         word_list = after.split("|")
#         try:
#             wl = np.array(word_list)
#             print((wl))
#             loc = np.where(wl == "報名˙")            
#             print(loc)
#             # for i in range(loc[0],loc[0]+10):
#             #     print(word_list[i],end = "")
#             print()
#         except ValueError as e:
#             print(content['id']+" does not exit 日期")
       

# cut_article()