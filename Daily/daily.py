import os
from datetime import datetime
import time
import platform
import subprocess

def get_python():
    os_name = platform.system()
    python_cmd = "python"
    if os_name == "Windows":
        python_cmd = "python"
    elif os_name == "Linux" or os_name == "Darwin":
        python_cmd = "python3"
    return python_cmd


def get_time_now():
    return datetime.now().strftime("%H:%M:%S")


def do_scan():
    parent_path = os.path.abspath(os.path.join(os.path.abspath(__file__) , ".." , ".."))

    spider_path = os.path.join(parent_path , "Spider")
    
    #run Spider
    for spiderFile in os.listdir(spider_path):
        spider_file_path = os.path.join(spider_path, spiderFile)
        if os.path.isfile(spider_file_path):
            subprocess.run([get_python() , spider_file_path])
    
    #run filter
    subprocess.run([get_python() , os.path.join(parent_path , "FilterTools" , "filter.py")])
    
    #post
    #subprocess.run([get_python() , os.path.join(parent_path , "Daily" , "post.py")])
    


while True:
    do_scan()
    break
    Time = get_time_now()
    print("\rtime:", Time, end="")
    if Time == "14:58:50":
        do_scan()
    time.sleep(1)
