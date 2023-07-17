import csv
from docx import Document
import os
import json
import re

global data_list 
data_list  = []

global chap_data_list
chap_data_list = []

# 提炼文本
def extract_details(docx_path, json_path):

    document = Document(docx_path)

    #json 
    #提取file name, used for pics 
    file_name = os.path.basename(docx_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    print(file_name_without_extension)

    # with open(json_path, 'r', encoding="utf-8") as file:
    #     json_data = json.load(file)

    data = {
        "name" : file_name_without_extension,
        # "img" : file_name_without_extension + ".jpg",
        "details" : []
    } 

    char_detail = {
        "identities" : [],
        "overview" : []
    }

    title = ""
    content = []

    isIden = False 

    for paragraph in document.paragraphs:
        line = paragraph.text.strip()
        # print(line)

        if not line:
            continue

        if ":" in line:
            if title and content != []: #reached start of next title
                if isIden: #身份内容
                    char_detail["identities"] = content
                else: #简介内容
                    char_detail["overview"] = content
                        

            title = line.split(":")[0]
            content = []

            if title == "身份":
                isIden = True

            elif title == "简介":
                isIden = False
            
        else: #continuous paragraph 
            content.append(line)
            
    if title and content != []: #end of doc
        if isIden: #身份内容
            char_detail["identities"] = content
        else: #简介内容
            char_detail["overview"] = content
        
    data["details"] = char_detail
    data_list.append(data)

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    return file_name_without_extension


def main():
    os.chdir('./关于charlie/charlie关系梳理')

    relationships = os.listdir()
    for re in relationships:
        extract_details(re,"../人物关系.json")


if __name__ == '__main__':
    main()
