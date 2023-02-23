#waiting for 2023 page
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

    driver = webdriver.Chrome(executable_path='./Tools/chromedriver.exe')

    driver.get(url)
    time.sleep(2)

    select = Select(driver.find_element(By.ID, "yearList"))

    select.select_by_index(1)
    time.sleep(5)
    OutputList = []
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
            "Title": title,
            "Content": string,
            "Sources": [url],
            "Images": [img],
        }
        OutputList.append(article)

        driver.find_element(
            By.XPATH, "//*[@id=\"tournaments\"]/div/div/div[1]/button/span[1]").click()
    with open("./FilterTools/SpiderData/CTESA.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputList , writeFile, ensure_ascii=False, indent=4)
    record_runtime(f"\nCTESA上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nCTESA上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
