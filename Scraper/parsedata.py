import json


with open("datafile.json") as file:
    jsonData = json.load(file)

count = 0
for i in jsonData:
    count = count + 1

print(count)