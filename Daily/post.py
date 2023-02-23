import os
import requests
import json
import math

IP = "220.132.244.41"
HOST = f"http://{IP}:5044/api/activity"

# SETTING
chop_group_num = 10  # 一次上傳的活動數
json_file_name = 'FilterAfter.json'  # 檔案名稱


def printProgressBar(now, total, length=20):
    progress = now/total
    progressValue = int((progress)*length)
    print("\r[%s%s] %d/%d" % (
        progressValue * "=",
        (length - progressValue) * " ",
        now,
        total
    ), end="")


def activity_controller_async(activity_list):
    finished_post = 0
    total_post = math.ceil(len(activity_list)/chop_group_num)

    for _ in range(total_post):
        result = post_activity_async(activity_list[0:chop_group_num])
        finished_post += 1
        printProgressBar(finished_post, total_post)
        print(f"\t [{result}]", end="")
        del activity_list[0:chop_group_num]

    print('\n完成')


def post_activity_async(post_list):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(HOST, json=post_list, headers=headers, timeout=5)
    if r.status_code == 400:
        
        with open("TEMP.json", "w", encoding="utf-8") as jsonFile:
            jsonFile.write(json.dumps(post_list, indent=4))
        exit()
    
    return r.status_code


parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
with open(os.path.join(parent_path, json_file_name), "r", encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    activity_controller_async(json_data)
