from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import requests

import time
import json
import os

import datetime
now = datetime.datetime.now()


def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)


try:
    url = "https://www.ctesa.com.tw/tournaments"

    resource_path = "./projects"

    if not os.path.exists(resource_path):
        os.mkdir(resource_path)

    driver = webdriver.Chrome(executable_path='./chromedriver.exe')

    driver.get(url)
    time.sleep(2)

    select = Select(driver.find_element(By.ID, "yearList"))

    select.select_by_index(1)
    time.sleep(5)

    for i in range(1, 8):
        driver.find_element(
            By.XPATH, "//*[@id=\"course\"]/div[3]/div[{}]/div[2]/a".format(i)).click()
        time.sleep(2)
        string = driver.find_element(
            By.XPATH, "//*[@id=\"tournaments\"]/div/div/div[2]").text
        image = driver.find_element(
            By.XPATH, "//*[@id=\"tournaments\"]/div/div/div[2]/div[1]/div[1]/img")
        title = driver.find_element(
            By.XPATH, "//*[@id=\"tournaments\"]/div/div/div[2]/div[1]/div[2]/div[1]/span").text
        img = image.get_attribute('src')

        article = {
            "source_web_name": "中華民國電子競技運動協會",
            "source_url": url,
            "url": None,
            "title": title,
            "content": string,
            "date": None,
            "image": [img],
            "id": 0,
        }

        if not os.path.isfile("./projects/index.json"):  # initailize the json file
            with open("./projects/index.json", "w") as InitialFile:
                InitialFile.write("[]")

        # transfer the article dic to json
        with open("./projects/index.json", "r", encoding="utf-8") as JsonFile:
            jsonDict = json.load(JsonFile)

        jsonDict.append(article)  # add all every dic in to this list

        # write this to the json file
        with open("./projects/index.json", "w",  encoding="utf-8") as writeFile:
            json.dump(jsonDict, writeFile, ensure_ascii=False, indent=1)

        driver.find_element(
            By.XPATH, "//*[@id=\"tournaments\"]/div/div/div[1]/button/span[1]").click()

    record_runtime(f"\nCTESA上次更新時間為:{now}\n\t執行成功")
except:
    record_runtime(f"\nCTESA上次更新時間為:{now}\n\t**執行失敗")
