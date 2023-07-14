import pymongo 
import json
import config

# 获取MongoDB Atlas连接字符串
#手动输入url
connection_string = client = config.ENCRYPTED_MONGODB_URL

# 创建MongoDB客户端
client = pymongo.MongoClient(connection_string)

# 连接到数据库
# db = client.Charlie
db = client.CharlieDB

#collections
truth_dare = db.truth_or_dare
day_night_chaps = db.day_and_night_chaps
day_night_subchaps = db.day_and_night_subchaps
dream_weaving = db.dream_weaving
merch = db.merch
furniture = db.furniture
volume = db.volume
profile_detail = db.profile_detail 
rewind = db.rewind
track = db.track
film_cards = db.film_cards
film_chaps = db.film_chaps
memories_album = db.memories_album


# # 插入数据
def read_one(collection, file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    collection.insert_one(data)

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
    read_many(memories_album,'./灵犀相册/灵犀.json')
    # delete_all(merch)
    # read_one(furniture,'./家具/furniture.json')
