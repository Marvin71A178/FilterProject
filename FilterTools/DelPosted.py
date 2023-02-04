import json

FilterAfter = []
with open("./Daily/FilterAfter.json" , "r", encoding="utf-8") as readFile:
    FilterAfter = json.load(readFile)

PostedActivity = []
with open("./FilterTools/PostedActivity.json", "r", encoding="utf-8") as readFile:
    PostedActivity = json.load(readFile)
    
NewActivities = []

for i in FilterAfter:
    if i["Title"] in PostedActivity:
        continue
    else:
        NewActivities.append(i)
        PostedActivity.append(i["Title"])

with open("./Daily/FilterAfter.json" , "w" , encoding="utf-8") as writeFile:
    json.dump(NewActivities , writeFile , ensure_ascii=False , indent=4)
with open("./FilterTools/PostedActivity.json" , "w" , encoding="utf-8") as writeFile:
    json.dump(PostedActivity , writeFile , ensure_ascii=False , indent=4)

        
    

    