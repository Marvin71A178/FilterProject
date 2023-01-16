#嘉義文化創意產業園區
import requests
from bs4 import BeautifulSoup
import itertools
import json

header ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

allActivity_set = set()
for i in itertools.count(start = 1):
    o_url = f"https://www.g9cip.com/category/activity/page/{i}/"
    res = requests.get(o_url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    for link in soup.select('article > div > div > div > section > div > div > div > div > div > div > a:not([rel])'):
        allActivity_set.add(link['href'])
    if res.status_code == 404:
        break
ActivityList = []
for url in allActivity_set:
    sub_url = url
    sub_res = requests.get(sub_url, headers = header)
    sub_soup = BeautifulSoup(sub_res.text, "html.parser")
    test_li = sub_soup.find_all("div", class_ = ["elementor-heading-title","elementor-size-default"])
    title_li = []
    content_li = []
    mainBody = sub_soup.select("body > div > section > div > div > div > section > div > div")
    img_url = []
    for fimg in mainBody :
        if fimg.get("data-settings") == '{"background_background":"classic","_ob_bbad_is_stalker":"no","_ob_teleporter_use":false,"_ob_column_hoveranimator":"no","_ob_column_has_pseudo":"no"}':
            imgli = fimg.select("img")
            for k in imgli:
                img_url.append(k["data-src"])
    for i in test_li :
        if i.find("a")==None:
            title_li.append(i.text)
        content_li.append(i.text)
    title = title_li[4]
    holder = ""
    for i in range(len(content_li)):
        if content_li[i] == "主辦單位":
            holder = content_li[i+1]
            break
            
    date = ""
    for i in range(len(content_li)):
        if content_li[i] == "日期":
            date = content_li[i+1]
            break
        
    site = ""
    for i in range(len(content_li)):
        if content_li[i] == "地點":
            site = content_li[i+1]
            break
    
    Activity_dic = {
        "Url" : url,
        "Title": title,
        "Date" : date,
        "Location" : site,
        "holder" : holder,
        "image" : img_url
            }
    
    ActivityList.append(Activity_dic)

with open("./G9CreativePark/projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
        json.dump( ActivityList , writeFile , ensure_ascii=False ,indent = 4 )


