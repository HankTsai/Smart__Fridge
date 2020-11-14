import pymongo

def mongo_connect_build():
    # 跟mongodb建立連線
    global mycol
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # client = pymongo.MongoClient(host="mongodb", port=27017)

    # 選擇使用的db,不存在則會在資料輸入時自動建立
    db = client['test11111111111111111']

    # 選擇collection,不存在則會在資料輸入時自動建立
    mycol = db["original-recipe"]

def data_insert(data):
    # # 輸入單筆資料
    # data_one = mycol.insert_one(data)
    # print(data_one)

    #多筆資料
    data_many = mycol.insert_many(data)
    print(data_many.inserted_ids)
    # 輸出輸入資料的ID

def data_find(myquery):
    # # 尋找第一筆資料
    # find_data = mycol.find_one()
    # # 尋找第一筆指定資料
    # find_data = mycol.find_one(myquery)
    # print(find_data)

    # # 尋找多筆指定資料
    # for find_manydata in mycol.find(myquery):
    #     print(find_manydata)

    # 尋找&秀出指定欄位 1為要顯示 , 0為不顯示
    for data_select in mycol.find((myquery), {"_id": 0, "recipe": 1, "tags": 1, "quantity":1}):
        print(data_select)

    # 下面會噴錯,不可同時指定1和0(除了id),若不顯示就不要打出來。(如果设置了一个字段为 0，则其他都为1)
    # for data_select in mycol.find({myquery}, {"_id": 0, "name": 1, "cn_name": 0}):
        # print(data_select)

def data_modify(oldquery,newquery):
    # # 修改內容 $set ,一次改一筆,從第一筆開始
    # print(mycol.update_one(oldquery, newquery))
    # 一次全改
    mycol.update_many(oldquery,newquery)
    for x in mycol.find():
        print(x)


def data_delete(mydelete):
    #刪除第一筆
    mycol.delete_one(mydelete)

    # #刪除多筆
    # mycol.delete_many(mydelete)
    #
    # #刪除全部
    # mycol.delete_many({})


if __name__ == '__main__':
    mongo_connect_build()



# #ex1:輸入單筆資料-字典
# data = {"recipe_id":"001", "recipe":"chicken"}
# data_insert(data)

# # ex2:輸入多項資料
# mylist = [
#     {"_id": 1, "name": "RUNOOB", "cn_name": "菜鸟教程"},
#     {"_id": 2, "name": "Google", "address": "Google 搜索"},
#     {"_id": 3, "name": "Facebook", "address": "脸书"},
#     {"_id": 4, "name": "Taobao", "address": "淘宝"},
#     {"_id": 5, "name": "Zhihu", "address": "知乎"} ]
# data_insert(mylist)

# #ex3: 查詢資料
# myquery = { "tags": "紅燒" }
# data_find(myquery)

# #ex4:條件查詢 (數量>6) *數量需做處理(int/str)
# myquery = { "quantity": { "$gt": "9" } }
# data_find(myquery)

# #ex5:re條件查詢(日式開頭食譜)
# myquery = { "recipe": { "$regex": "^日式" } }
# data_find(myquery)

# # ex6: 字典修改(oldoldquery=欲修改欄位; newquery=欲更改的值
# oldquery = {"like":0}
# newquery = {"$set": {"like":00}}
# data_modify(oldquery,newquery)

# ex7: 刪除指定資料
mydelete = {"_id":5}
data_delete(mydelete)

