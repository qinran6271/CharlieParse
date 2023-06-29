import pymongo 
import json

# 获取MongoDB Atlas连接字符串
#手动输入url
connection_string = client = ""

# 创建MongoDB客户端
client = pymongo.MongoClient(connection_string)

# 连接到数据库
# db = client.Charlie
db = client.CharlieDB

# 真心话大冒险collection
truth_dare = db.truth_or_dare

# # 插入数据
# collection.insert_one(data)

# 多个json文档读取
def read_many(collection, file_name):
    with open(file_name) as file:
        file_content = file.read()
        json_data = json.loads(file_content)
        # 插入到 MongoDB 中
        collection.insert_many(json_data)

# 删除当前collection所有object
def delete_all(collection):
    collection.delete_many({})

if __name__ == '__main__':
    read_many(truth_dare,'./真心话/tod.json')
    # delete_all( truth_dare)
