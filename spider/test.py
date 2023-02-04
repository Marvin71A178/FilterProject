#私立二信高級中學
import requests
from bs4 import BeautifulSoup
import itertools
import os
import json
from requests.adapters import HTTPAdapter
import datetime
now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord" , "a", encoding="utf-8") as writefile:
        writefile.write(text)
        
        
        
def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")


headers  = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

url = "https://esshb.essh.kl.edu.tw/%E5%A4%9A%E5%85%83%E5%AD%B8%E7%BF%92%E8%B3%87%E8%A8%8A%E7%AB%99/?lcp_page0=%7B%7D&lcp_page0=33#lcp_instance_0"

res = requests.get(url , headers=headers)
print(res.status_code)

