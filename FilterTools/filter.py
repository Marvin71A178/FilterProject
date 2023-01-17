import json
import re
import copy
import datetime
import os


def load_json_folder(folder_road):
    f = open(folder_road, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


branchKey = load_json_folder("./FilterTools/Keys/branch_key.json")
ex_branchKey = load_json_folder("./FilterTools/Keys/ex_branch_key.json")
tagKey = load_json_folder("./FilterTools/Keys/tags_key.json")


class Activity():
    def __init__(self, DictFromSpider):
        self.DictFromSpider = DictFromSpider
        self.Title = None
        self.Content = None
        self.Images = None
        self.Connection = None
        self.Holder = None
        self.Objective = None
        self.Sources = None
        self.Subtitle = None
        self.Tags = None
        self.Branches = None
        self.Date = None
        self.Location = None
        self.Id = 0

    # return要寫入json的資料
    def OutputFormat(self):
        Dict = {
            "Title": self.Title,
            "Content": self.Content,
            "Images": self.Images,
            "Connection": self.Connection,
            "Holder": self.Holder,
            "Objective": self.Objective,
            "Sources": self.Sources,
            "Subtitle": self.Subtitle,
            "Tags": self.Tags,
            "Branches": self.Branches,
            "Id": self.Id
        }
        return Dict

    def TitleFilter(self):
        self.Title = self.DictFromSpider["Title"]
        return

    def ContentFilter(self):
        # if self.DictFromSpider["Content"] == None:
        #     print(123)
        self.Content = self.DictFromSpider["Content"]
        return

    def ImagesFilter(self):
        self.Images = self.DictFromSpider["Images"]
        return

    def ConnectionFilter(self):
        self.Connection = self.DictFromSpider["Connection"]
        return

    def HolderFilter(self):
        self.Holder = self.DictFromSpider["Holder"]
        return

    def ObjectiveFilter(self):
        self.Objective = self.DictFromSpider["Objective"]
        return

    def SourcesFilter(self):
        temSources = set()
        url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9@:%_\\+.~#?&\\/=]*)"
        # 處理爬蟲下來的連結
        
        for spiderSources in self.DictFromSpider["Sources"]:
            for x in re.findall(url_extract_pattern, spiderSources):
                temSources.add(x)
        # 處理內文含有的連結
        res = isinstance(self.Content, str)
        if (res):
            for x in re.findall(url_extract_pattern, self.Content):
                temSources.add(x)
        # 由set過濾 以list儲存
        if None in temSources:
            temSources.remove(None)

        self.Sources = list(temSources)
        return

    def SubtitleFilter(self):
        self.Subtitle = self.DictFromSpider["Subtitle"]
        return

    def TagsFilter(self):
        self.Tags = self.DictFromSpider["Tags"]
        return

    def BranchesFilter(self):
        self.Branches = self.DictFromSpider["Branches"]
        return

    def DateFilter(self):
        self.Date = self.DictFromSpider["Date"]
        return

    def LocationFilter(self):
        self.Location = self.DictFromSpider["Location"]
        return

    def Initialize(self):
        for keys in self.DictFromSpider:
            eval("self."+keys+"Filter()")


# 讀入所有json
directory = './FilterTools/SpiderData'
OutputActivityList = []
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        Loads = load_json_folder(f"{directory}/{filename}")
        for Load in Loads:
            # 將每一個爬出來的dict弄成class
            Output = Activity(Load)
            Output.Initialize()
            OutputActivityList.append(Output.OutputFormat())
# 寫入json
with open("./Daily/FilterAfter.json", "w", encoding="utf-8") as writeFile:
    json.dump(OutputActivityList, writeFile, ensure_ascii=False, indent=4)
