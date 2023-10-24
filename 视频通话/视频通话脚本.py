from docx import Document
import os
import json
import pymongo

# 防止重复加入数据库
insertDatabase = False


def main():
    all_data = []           # 总数据
    data = {
        "name": "",         # 文本标题
        "entry": "",        # 文本目录
        "videoLink": "",    # 视频链接
        "content": [],      # 对话内容
    }

    # 提取文本内容
    for filename in os.listdir("文本"):
        if filename == ".DS_Store":
            continue
        document = Document("文本/" + filename)
        filetitle = filename.split('-')[1].split('.')[0]
        entry = filename.split('-')[0]

        videoLink = ""
        content = []
        for paragraph in document.paragraphs:
            line = paragraph.text.strip()
            if not line:
                continue
            if "视频链接:" in line or "查理苏" in line:
                continue
            if "www.bilibili.com" in line:
                videoLink = line
                continue
            content.append(line)

        data["name"] = filetitle
        data["entry"] = entry
        data["videoLink"] = videoLink
        data["content"] = content
        all_data.append(data.copy())

    # 总数据转成json
    with open("视频通话" + ".json", "w", encoding="utf-8") as outfile:
        json.dump(all_data, outfile, ensure_ascii=False, indent=4)

    # 加入数据库
    if insertDatabase:
        client = pymongo.MongoClient("mongodb://CharlieDB0724:Charlie0724@47.243.195.59/CharlieDB")
        db = client["CharlieDB"]
        col = db["video_call"]
        col.insert_many(all_data)

    return 0


if __name__ == '__main__':
    main()
