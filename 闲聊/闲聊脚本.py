import csv
from docx import Document
import os
import json
import re
import uuid

global details_data_list 
data_list = []

# 提炼小节文本
def extract_content(docx_path):

    document = Document(docx_path)

    #提取file name
    file_name = os.path.basename(docx_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    data = {
        "chat_name": file_name_without_extension, #闲聊名称
        "video" : "",
        "chat_content":[]
    }

    choice_region = {
        "type": "choice",
        "region_content": []
    }


    speaker = ""
    content = []
    current_list = data["chat_content"]
    regular = True 

    for paragraph in document.paragraphs:
        line = paragraph.text.strip()

        if not line:
            continue

        if ":" in line:
            if speaker and content: #reached start of next dialogue 

                if regular:
                    current_list.append({
                        "type": "normal",
                        "speaker": speaker, #我 or 查理苏
                        "content": content #讲话内容
                    })
                    content = []
                else:
                    current_list.append({
                        "speaker": speaker, #我 or 查理苏
                        "content": content #讲话内容
                    })
                    content = []
            

            speaker,choice_name = line.split(":")[0], line.split(":")[1]


            if speaker == "https":
                data["video"] = line


            elif speaker == "区域开始":  
                regular = False

            elif speaker == "Choice":
                choice = {
                        "choice_name": choice_name, # 选项名称
                        "choice_content": [
                        ]
                    }
                choice_region["region_content"].append(choice)
                current_list = choice["choice_content"]
                content = []  
                # if int(choice_name) > 1:
                #     choice_content.append(choice_obj)

        elif "区域结束" in line:
            if speaker and content:
                regular = True  
                current_list.append({
                        "type": "normal",
                        "speaker": speaker, #我 or 查理苏
                        "content": content #讲话内容
                    })
                data["chat_content"].append(choice_region)
                choice_region = {
                    "type": "choice",
                    "region_content": []
                }
                content = [] 
                current_list = data["chat_content"] 


        else: #continuous paragraph 
            content.append(line)
            

            
    if speaker and content:
                
        if regular:
            current_list.append({
                "type": "normal",
                "speaker": speaker, #我 or 查理苏
                "content": content #讲话内容
            })
            content = []
        else:
            current_list.append({
                "speaker": speaker, #我 or 查理苏
                "content": content #讲话内容
            })
            content = []


    data_list.append(data)
    data_json = "../chat.json"


    with open(data_json, "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    return 


def sort_by_integer(filename):
    # 使用正则表达式提取文件名中的整数部分
    match = re.match(r'(\d+)-', filename)
    if match:
        number = int(match.group(1))
        return number
    return 10000  # 如果文件名不符合格式要求，则返回 0 进行排序

def main():
    os.chdir('./闲聊') #mark data as root dir
    doc_path = './闲聊demo.docx'

    # types = sorted(os.listdir(),key=sort_by_integer) #find all subdirs / chapters & sort
    # types = os.listdir()
    # # print(types)
    # for type_name in types: 
    #     type_path = './' + type_name
       

        # subchap_nums = [] # 储存当前所有小节的编号
        # ending= []

        # type_list = os.listdir(type_path)

        # 填充type聊天记录的总数
        # para_type_data["totalNum"] = len(type_list)
    

    extract_content(doc_path)



    # filename = './主线文本/7-13'  # 请将此路径替换为您的docx文件路径
    # docx_path = filename + '.docx'
    
    # json_path = "test" + ".json"
    # extract_content(docx_path, json_path)
    
    

if __name__ == '__main__':
    main()
