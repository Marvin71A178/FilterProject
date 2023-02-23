import requests
import json
from http.cookies import SimpleCookie
from urllib.parse import unquote
import base64
from bs4 import BeautifulSoup
import datetime
now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)
def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("__ AiCamp\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")
token_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Referer": "https://aicamp.com.tw/",
    "Origin": "https://aicamp.com.tw",
}
try:
    token_request = requests.get("https://aicamp.com.tw/cart/get", headers=token_headers)

    # print("更新Token:\t",token_request.status_code)
    # 把 cookie 字串 變成 dict
    cookie = SimpleCookie()
    cookie.load(token_request.headers["Set-Cookie"])
    cookies = {k: v.value for k, v in cookie.items()}

    # 獲取 cookie & token 
    session_token = cookies["aicamp_session"]
    x_xsrf_token = cookies['XSRF-TOKEN']
    x_2_token = cookies['XSRF-TOKEN'].replace("%3D", "=")

    # 驗證 檔頭 (header)
    url = "https://aicamp.com.tw/api/course/query"
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": x_2_token,
        "Cookie":f"aicamp_session={session_token}; _gcl_au=1.1.520515681.1675848080; _ga_RMEPEE48TR=GS1.1.1675860405.3.1.1675862105.60.0.0; _ga=GA1.3.961938519.1675848080; _ga_SCSL6CP2X2=GS1.1.1675860405.3.1.1675862105.60.0.0; _gid=GA1.3.1566165878.1675848081; need-cookie=1; XSRF-TOKEN={x_xsrf_token}; _gat_UA-181674063-2=1",
        "Connection": "keep-alive",
        "Referer": "https://aicamp.com.tw/",
        "Origin": "https://aicamp.com.tw"
    }
    Data = {"page":1,
            "pageSize":8,
            "category_id":"",
            "category_sub":"",
            "type_id":"","class_city_id":"","organizer_id":"","gather_id":"","keyword":"","price":"","days":"","factors":"[]","begin_date":"","end_date":"","sort_order_view":"","sort_order_time":"","sort_order_price":"","sort_order_days":""}


    r = requests.post(url, headers=headers , json=Data)
    # print("獲取資料", r.status_code)

    # 獲取資料
    jsonlist = json.loads(r.content.decode("utf-8"))

    total = jsonlist["data"]["total"]
    Data["pageSize"] = total
    r = requests.post(url, headers=headers , json=Data)
    jsonlist = json.loads(r.content.decode("utf-8"))
    OutputActivity = []
    finished_post = 0
    for i in jsonlist["data"]["data"]:
        finished_post += 1
        printProgressBar(finished_post , len(jsonlist["data"]["data"]))
        o_url = i["url"]
        html = i["description"]
        if html == None:
            continue
        soup = BeautifulSoup(html , "html.parser")

        Contents = soup.find_all(text=True)
        Content = "\n".join(Content.strip() for Content in Contents)
        if Content == "":
            continue
        dic = {
            "Title": i["name"],
            "Content" : Content,
            "html" : base64.b64encode(str(soup).encode("utf-8")).decode('utf-8'),
            "Sources" : [i["url"]]
        }
        if i["pic_url"] != None:
            dic["Images"] = [i["pic_url"]]
        if i["link"] != None:
            dic["Sources"].append(i["link"])
        OutputActivity.append(dic)

    # 寫入 json 檔案
    # fp = open("./test.json", "w", encoding="utf-8")
    # json.dump(jsonlist, fp, indent=4, ensure_ascii=False)
    with open("./FilterTools/SpiderData/AiCamp.json", "w", encoding="utf-8") as writeFile:
        json.dump(OutputActivity , writeFile , ensure_ascii=False, indent=4)

    record_runtime(f"\nAiCamp上次更新時間為:{now}\n\t執行成功")
except Exception as e:
    record_runtime(f"\nAiCamp上次更新時間為:{now}\n\t**執行失敗\n\t\t{e}")
   