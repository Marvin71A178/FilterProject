import json
import re
import datetime
import os


now = datetime.datetime.now()
def record_runtime(text):
    with open("./Daily/DailyRecord", "a", encoding="utf-8") as writefile:
        writefile.write(text)
# try:
def load_json_folder(folder_road):
    f = open(folder_road, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data
def del_open_character(findall_list):
    tem = ""
    lineopen = ["一", "二", "三", "四", "五", "六", "七", "八", "九",
                "十", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖", "拾"]
    if findall_list[0][0] == "(" and findall_list[0][1] in lineopen and findall_list[0][2] == ")":
        for i in range(3, len(findall_list[0])):
            tem += findall_list[0][i]
        findall_list[0] = tem
    elif findall_list[0][0] in lineopen and findall_list[0][1] == "、":
        for i in range(2, len(findall_list[0])):
            tem += findall_list[0][i]
        findall_list[0] = tem
    elif findall_list[0][1] in lineopen and findall_list[0][2] == "、":
        for i in range(3, len(findall_list[0])):
            tem += findall_list[0][i]
        findall_list[0] = tem

branchKey = load_json_folder("./FilterTools/Keys/branch_key.json")
ex_branchKey = load_json_folder("./FilterTools/Keys/ex_branch_key.json")
tagKey = load_json_folder("./FilterTools/Keys/tags_key.json")

def ex_branch_filter(content_list,data,key):
    
    returnList = []
    for value in data[key]:
        for content_in_line in content_list:
            findall_list = re.findall(value, content_in_line)
            if len(findall_list) != 0:
                tem = ""
                while findall_list[0][0] == "%":
                    for i in range(1, len(findall_list[0])):
                        tem += findall_list[0][i]
                    findall_list[0] = tem
                    tem = ""
                while findall_list[0][len(findall_list[0])-1] == "%":
                    for i in range(0, len(findall_list[0])-1):
                        tem += findall_list[0][i]
                    findall_list[0] = tem
                    tem = ""
                del_open_character(findall_list)
            if len(findall_list) != 0:
                returnList.extend(findall_list)
    if len(returnList) == 0:
        returnList = None
    return returnList
def tags_filter(content,data):
    tags_type_list = ["area", "location", "other"]
    tag_list = []
    tag_id = 0
    for type in tags_type_list:
        for tag in data[type]:
            if tag in content:
                tag_dic = {}
                tag_dic["Type"] = type
                tag_dic["Id"] = tag_id
                # tag_id += 1
                tag_dic["Text"] = tag
                tag_dic["TagCount"] = 1
                tag_list.append(dict(tag_dic))
                tag_dic.clear()
    if len(tag_list) == 0:
        return None
    else:
        return tag_list



class Activity():
    def __init__(self, DictFromSpider):
        self.DictFromSpider = DictFromSpider
        self.Title = DictFromSpider["Title"]
        self.Content = DictFromSpider["Content"]
        self.html = DictFromSpider["html"]
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
        
        self.Content_list = None

    # return要寫入json的資料
    def OutputFormat(self):
        
        Dict = {
            "Title": self.Title,
            "Content": self.html,
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
        if (not self.DictFromSpider.get("Title", False)) or self.DictFromSpider["Title"] == "":
            ##unfinish: try except throw Error
            print("no Title Error")
        else:
            self.Title = self.DictFromSpider["Title"]
        return

    def ContentFilter(self):
        if (not self.DictFromSpider.get("Content", False)) or self.DictFromSpider["Content"] == "":
            ##unfinish: try except throw Error
            print("no Content Error")
            print(self.Title)
        else:
            self.Content = self.DictFromSpider["Content"]
            content = self.Content
            content = "%" + content.replace("\n", "%↑%") + "%"
            self.Content_list = content.split("↑")
        return

    def ImagesFilter(self):
        if self.DictFromSpider.get("Images"):
            self.Images = self.DictFromSpider["Images"]
        return

    def ConnectionFilter(self):
        # print(self.DictFromSpider)
        self.Connection = ex_branch_filter(content_list=self.Content_list , data = ex_branchKey , key="Connection")  
        return

    def HolderFilter(self):
        if self.DictFromSpider.get("Holder", False):
            self.Holder = [self.DictFromSpider["Holder"]]
        else:
            self.Holder = ex_branch_filter(content_list=self.Content_list , data = ex_branchKey , key="Holder")  
            
        return

    def ObjectiveFilter(self):
        self.Objective = ex_branch_filter(content_list=self.Content_list , data = ex_branchKey , key="Objective")  
        return

    def SourcesFilter(self):
        temSources = set()
        url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9@:%_\\+.~#?&\\/=]*)"
        
        # 處理爬蟲下來的連結
        for spiderSources in self.DictFromSpider["Sources"]:
            # print(spiderSources)
            for x in re.findall(url_extract_pattern, spiderSources):
                temSources.add(x)
        
        # 處理內文含有的連結
        for x in re.findall(url_extract_pattern, self.Content):
            temSources.add(x)
                
        # 由set過濾 以list儲存
        if None in temSources:
            temSources.remove(None)

        self.Sources = list(temSources)
        return

    def SubtitleFilter(self):
        if self.DictFromSpider.get("Subtitle", False):
            self.Subtitle = self.DictFromSpider["Subtitle"]
        return

    def TagsFilter(self):
        self.Tags = tags_filter(content=self.Content , data = tagKey)
        return

    def BranchesFilter(self):
        
        def to_date_type(name, li, content):
            if li == None:
                return li
            list2 = []

            for i in range(0, len(li)):
                check = True
                for j in range(0, len(li)):
                    if i != j:
                        if (li[i] in li[j]):
                            check = False
                if check:
                    list2.append(li[i])

            li = list2
            if name == "DateStart":
                datestart_dic = {}
                space = ""
                GeneralDateStart = "GeneralDateStart"
                for line in li:
                    find_key_name = re.findall(
                        "[\u4E00-\u9FFF^報][\u4E00-\u9FFF^名]日期", line)
                    split_list = re.split("[^0-9]", line)
                    remove_split_list = [i for i in split_list if i != ""]
                    date = ""
                    try:
                        if "即日" in line:
                            datestart_dic[GeneralDateStart] = "自即日起"
                            GeneralDateStart += "."
                            continue
                        elif len(remove_split_list) == 2:
                            year4 = re.findall(
                                "[^0-9]{0,1}[0-9]{4}年", content)
                            year3 = re.findall(
                                "[^0-9]{0,1}[0-9]{3}年", content)
                            if len(year4) != 0:
                                year = re.findall("[0-9]{4}", year4[0])
                                date = str(datetime.date(int(year[0]), int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            elif len(year3) != 0:
                                year = re.findall("[0-9]{3}", year3[0])
                                date = str(datetime.date(int(year[0])+1911, int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            else:
                                date = line
                        elif len(remove_split_list) == 3:
                            if int(remove_split_list[0]) < 1911:
                                remove_split_list[0] = str(
                                    int(remove_split_list[0])+1911)
                            date = str(datetime.date(int(remove_split_list[0]), int(
                                remove_split_list[1]), int(remove_split_list[2])))
                        else:
                            date = line

                    except ValueError:
                        date = line
                    findkey = ["決賽", "初賽", "線上賽", "線下賽"]
                    if len(find_key_name) == 0:
                        for name in findkey:
                            if name in line:
                                find_key_name = [name]
                    if len(find_key_name) != 0:
                        datestart_dic[find_key_name[0] + space] = date
                        space += "."
                    else:
                        datestart_dic[GeneralDateStart] = date
                        GeneralDateStart += "."

                # if len(datestart_dic["GeneralDateStart"]) == 0:
                #     del datestart_dic["GeneralDateStart"]
                return datestart_dic

            if name == "ApplyStart":
                date = ""
                returnlist = []
                for line in li:
                    split_list = re.split("[^0-9]", line)
                    remove_split_list = [i for i in split_list if i != ""]
                    try:
                        if "即日" in line:
                            returnlist.append("自即日起")
                            continue
                        elif len(remove_split_list) == 2:
                            year4 = re.findall(
                                "[^0-9]{0,1}[0-9]{4}[年]", content)
                            year3 = re.findall(
                                "[^0-9]{0,1}[0-9]{3}[年]", content)
                            if len(year4) != 0:
                                year = re.findall("[0-9]{4}", year4[0])
                                date = str(datetime.date(int(year), int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            elif len(year3 != 0):
                                year = re.findall("[0-9]{3}", year3[0])
                                date = str(datetime.date(int(year)+1911, int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            else:
                                date = line
                        elif len(remove_split_list) == 3:
                            if int(remove_split_list[0]) < 1911:
                                remove_split_list[0] = str(
                                    int(remove_split_list[0])+1911)

                            date = str(datetime.date(int(remove_split_list[0]), int(
                                remove_split_list[1]), int(remove_split_list[2])))
                        else:
                            date = line

                    except:
                        date = line
                    returnlist.append(date)
                    # returnlist.clear()
                # list(dict.fromkeys(returnlist))
                return returnlist
            if name == "DateEnd" or name == "ApplyEnd":
                date = ""
                returnlist = []
                to_key = ["到.{0,20}", "至.{0,20}", "-.{0,20}", "~.{0,20}", "test"]
                for line in li:
                    afterline = []
                    for keys in to_key:
                        if len(afterline) == 0:
                            afterline = re.findall(keys, line)

                        else:
                            split_list = re.split("[^0-9]", afterline[0])
                            remove_split_list = [i for i in split_list if i != ""]
                            try:
                                if len(remove_split_list) == 1:
                                    test1 = re.findall("[0-9]{4}年[0-9]{1,2}月", line)
                                    test2 = re.findall("[0-9]{4}/[0-9]{1,2}", line)
                                    test3 = re.findall("[0-9]{3}年[0-9]{1,2}月", content)
                                    test4 = re.findall("[0-9]{3}/[0-9]{1,2}", content)
                                    if len(test1) != 0:
                                        split_list = re.split(
                                            "[^0-9]", test1[0] + afterline[0])
                                        remove_split_list = [
                                            i for i in split_list if i != ""]
                                        date = str(datetime.date(int(remove_split_list[0]), int(
                                            remove_split_list[1]), int(remove_split_list[2])))
                                    elif len(test2) != 0:
                                        split_list = re.split(
                                            "[^0-9]", test2[0] + afterline[0])
                                        remove_split_list = [
                                            i for i in split_list if i != ""]
                                        date = str(datetime.date(int(remove_split_list[0]), int(
                                            remove_split_list[1]), int(remove_split_list[2])))

                                    elif len(test3) != 0:
                                        split_list = re.split(
                                            "[^0-9]", test3[0] + afterline[0])
                                        remove_split_list = [
                                            i for i in split_list if i != ""]
                                        date = str(datetime.date(int(
                                            remove_split_list[0])+1911, int(remove_split_list[1]), int(remove_split_list[2])))

                                    elif len(test4) != 0:
                                        split_list = re.split(
                                            "[^0-9]", test4[0] + afterline[0])
                                        remove_split_list = [
                                            i for i in split_list if i != ""]
                                        date = str(datetime.date(int(
                                            remove_split_list[0])+1911, int(remove_split_list[1]), int(remove_split_list[2])))
                                    else:
                                        date = line
                                    returnlist.append(date)
                                    break
                                elif len(remove_split_list) == 2:
                                    year4 = re.findall(
                                        "[^0-9]{0,1}[0-9]{4}[年]", line)
                                    year3 = re.findall(
                                        "[^0-9]{0,1}[0-9]{3}[年]", line)
                                    allyear4 = re.findall(
                                        "[^0-9]{0,1}[0-9]{4}[年]", content)
                                    allyear3 = re.findall(
                                        "[^0-9]{0,1}[0-9]{3}[年]", content)
                                    if len(year4) != 0:
                                        year = re.findall("[0-9]{4}", year4[0])
                                        date = str(datetime.date(int(year[0]), int(remove_split_list[0]), int(
                                            remove_split_list[1])))
                                    elif len(year3) != 0:

                                        year = re.findall("[0-9]{3}", year3[0])
                                        date = str(datetime.date(int(year[0])+1911, int(remove_split_list[0]), int(
                                            remove_split_list[1])))
                                    elif len(allyear4) != 0:
                                        year = re.findall("[0-9]{4}", allyear4[0])
                                        date = str(datetime.date(int(year[0]), int(remove_split_list[0]), int(
                                            remove_split_list[1])))
                                    elif len(allyear3) != 0:
                                        year = re.findall("[0-9]{3}", allyear3[0])
                                        date = str(datetime.date(int(year[0])+1911, int(remove_split_list[0]), int(
                                            remove_split_list[1])))
                                    else:
                                        date = line
                                elif len(remove_split_list) == 3:
                                    if int(remove_split_list[0]) < 1911:
                                        remove_split_list[0] = str(
                                            int(remove_split_list[0])+1911)
                                    # print("\033[91m" + remove_split_list[2] + "\033[0m")
                                    date = str(datetime.date(int(remove_split_list[0]), int(
                                        remove_split_list[1]), int(remove_split_list[2])))
                                else:
                                    date = line

                            except ValueError:
                                date = line
                            except:
                                date = line
                                # print("error")
                            returnlist.append(date)
                            break
                # list(dict.fromkeys(returnlist))
                return returnlist
        def regular_expression(branch_name, content, only_one):
            data = branchKey
            branch = {}
            content = "%" + content.replace("\n", "%↑%") + "%"
            content_in_line = content.split("↑")
            to_datetype_name = ["DateStart", "DateEnd", "ApplyStart", "ApplyEnd"]
            key_list = data[branch_name].keys()
            branch["BranchName"] = branch_name
            if only_one:
                branch_name = "OnlyOne"
            for output_key in key_list:
                branch[output_key] = None
                for key in data[branch_name][output_key]:
                    for contentinline in content_in_line:
                        findall_list = re.findall(key, contentinline)

                        if len(findall_list) != 0:
                            tem = ""
                            while findall_list[0][0] == "%":
                                for i in range(1, len(findall_list[0])):
                                    tem += findall_list[0][i]
                                findall_list[0] = tem
                                tem = ""
                            while findall_list[0][len(findall_list[0])-1] == "%":
                                for i in range(0, len(findall_list[0])-1):
                                    tem += findall_list[0][i]
                                findall_list[0] = tem
                                tem = ""
                            del_open_character(findall_list)
                        if len(findall_list) == 0:
                            findall_list = None
                        if branch[output_key] == None:
                            branch[output_key] = findall_list
                        elif findall_list != None:
                            for compare_twice in findall_list:
                                if not (compare_twice in branch[output_key]):
                                    branch[output_key].append(compare_twice)
                if output_key in to_datetype_name:

                    branch[output_key] = to_date_type(
                        output_key, branch[output_key], content)
            return branch
        def fil_branch(content):
            content.replace("\n", "%")
            branch_name_data = ["初賽", "複賽", "決賽", "線上賽", "線下賽"]
            branch_name_list = []
            for branch_name in branch_name_data:
                if (branch_name in content):
                    branch_name_list.append(branch_name)
            only_one = False
            if len(branch_name_list) == 0:
                branch_name_list.append("General")
            elif len(branch_name_list) == 1:
                only_one = True

            branches = []
            for branch_name in branch_name_list:
                regular_expression(
                    branch_name, content, only_one)
                branches.append(regular_expression(branch_name, content, only_one))

            return branches

        content = self.Content.replace(" ", "")
        self.Branches = fil_branch(content = content)
        for Branch in self.Branches:
            Branch["Status"] = None
        return

    def IdFilter(self):
        self.Id = 0
        return

    def Initialize(self):
        for needOutput in self.OutputFormat().keys():
            eval("self."+ needOutput +"Filter()")


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

record_runtime(f"\nfilter上次執行時間為:{now}\n\t執行成功")
# except Exception as e:
#     record_runtime(f"\nfilter上次執行時間為:{now}\n\t**執行失敗\n\t\t{e}")
#     print(e)