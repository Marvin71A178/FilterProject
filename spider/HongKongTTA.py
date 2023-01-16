#香港卓藝協會
import requests
from bs4 import BeautifulSoup
import os 
import json


o_url = "https://tta.hk/"

titles = []
urls = []


resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)


header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

res = requests.get(o_url,header)
soup = BeautifulSoup(res.text,"html.parser")

entrys = soup.find_all("h1",class_ = "elementor-heading-title elementor-size-default")

for entry in entrys:
    try:
        urls.append(entry.a['href'])
        titles.append(entry.text)
    except TypeError as e:
        continue



for url in urls:

    res_next = requests.get(url,header)
    soup_next = BeautifulSoup(res_next.text,"html.parser")

    im_url = soup_next.find_all("div" , class_ = "elementor-image")[1]

    images = im_url.img['data-srcset'].split(", ")
    image_list = []
    for image in images:
        image_list.append(image.split(" ")[0])

    contents = soup_next.find_all("div",class_ = "elementor-text-editor elementor-clearfix")
    content_list = []


    for content in contents:

        content_list.append(content.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))

        if content.text[0:6] == "比賽獎項 :":
            break
    content_str = ' '.join(content_list)

    article = {
        "source_web_name":"香港卓藝協會",
        "source_url":o_url,
        "url" : url,
        "title" : titles[urls.index(url)],
        "content" : content_str,
        "date" : None,
        "image":image_list,
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