import pymongo
import json
import os

global mycol
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['proposal_my_refrigerator']
mycol = db["original-recipe"]


yourPath = './climbing_recipe/'
# 列出指定路徑底下所有檔案(包含資料夾)
allFileList = os.listdir(yourPath)
# print(allFileList)

for i in allFileList:
    with open(r'./climbing_recipe/'+ i, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())
        data_many = mycol.insert_many(content)
        print(data_many)