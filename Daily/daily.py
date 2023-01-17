import os
import sys
from datetime import date, datetime
import time
from concurrent.futures import ThreadPoolExecutor


def get_python():
    os_name = sys.platform
    pythonExe = ""
    if os_name.lower() == "linux":
        pythonExe = "python3"
    elif os_name.lower() == "windows":
        pythonExe = "python"
    return pythonExe


def get_time_now():
    return datetime.now().strftime("%H:%M:%S")


def do_scan():
    parent_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))

    dict_path = {"camping": "camp.py", "ChanhuaGirls": "highSchool.py", "darts": "dart.py", "developerWeb": "webProject.py", "erXing": "erXingHigh.py", "G9CreativePark": "G9CreativeParkCrawler.py",
                 "game": "game.py", "hongKong": "hongkong.py", "hunter": "hunter.py", "jianguoHighSchool": "jianguo.py", "meseum": "museum.py", "peaceHighSchool": "PeaceHighSchool.py", "taoCulture": "taoCul.py", "re_filter_tool": "test.py"}

    for key, value in dict_path.items():
        workpath = os.path.join(parent_path, key)
        os.system(f"cd \"{workpath}\" && {get_python()} \"{value}\"")


while True:
    Time = get_time_now()
    print("\rtime:", Time, end="")
    if Time == "20:42:00":
        do_scan()
    time.sleep(1)
