#賞金獵人
import json
import re
import copy
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
try:
    
    load = open("./projects/filter.json", 'r' , encoding="utf-8" )
    js = json.load(load)
    load.close()
    length = len(js)
    all_url = []

    load2 = open("./projects/filter_after.filter_after.json" , "r" ,encoding="utf-8")
    js2 = json.load(load2)
    load2.close()

    for i in js:
        all_url.append(i['source'][0])

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = './chromedriver.exe',options=chrome_options)


    for url in all_url:
        driver.get(url)
        contents = driver.find_elements(By.CLASS_NAME,"ck-content")
        string = ""
        for content in contents:
            string+=content.text+"\n"

        article ={
            "source_web_name":"獎金獵人",
            "source_url": "https://bhuntr.com/tw",
            "url" : url,
            "title" : js[all_url.index(url)]["Title"],
            "content" : string,
            "date":None,
            "image":js[all_url.index(url)]["Image"],
            "Id": 0
        }
        
        if not os.path.isfile("./projects/index.json"): # initailize the json file
            with open("./projects/index.json", "w") as InitialFile:
                InitialFile.write("[]")

            
        with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 


        jsonDict.append(article) #add all every dic in to this list
            
        with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )

                
    record_runtime(f"\nHunter上次更新時間為:{now}\n\t執行成功")
except:
    record_runtime(f"\nHunter上次更新時間為:{now}\n\t**執行失敗")
