import pymongo 
import json
import config
import bson

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
chat_calls = db.chat_calls
chat_overview = db.chat_overview
chat_details= db.chat_details
moments_details = db.moments_details
moments_overview = db.moments_overview
talk = db.talk
vinyl = db.vinyl
characters = db.characters
charlie_details = db.charlie_details
date_overview = db.date_overview
date_details = db.date_details





# # 插入数据
def read_one(collection, file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    # 将JSON数据转换为Python字典
    
    collection.insert_one(data)   
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


    # delete_all(chat_calls)
    # delete_all(chat_overview)
    # delete_all(merch)
    # read_many(merch,'./谷子/新谷子.json')

    # delete_all(date_details)
    # delete_all(day_night_chaps)
    # delete_all(day_night_subchaps)
    read_many(characters,'./关于charlie/人物关系1.json')
    # read_many(date_details,'./记忆-约会/dateDB.json')
    # read_many(day_night_chaps,'./主线/chaps.json')
    # read_many(day_night_subchaps,'./主线/subchaps.json')
    # read_one(date_overview,'./记忆-约会/date_overview.json')



    # 查询所有subchap为11-2的文档
    # query = {"subchap_name": "11-2"}
    # results = day_night_subchaps.find(query)

    # # 更新subchap为11-2的文档为11-3
    # for result in results:
    #     day_night_subchaps.update_one({"_id": result["_id"]}, {"$set": {"subchap_name": "11-3"}})
