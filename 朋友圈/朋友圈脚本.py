import csv
from docx import Document
import os
import json
import re

global subchap_data_list 
subchap_data_list  = []

global chap_data_list
chap_data_list = []

# 提炼小节文本
def extract_details(indexCode, docx_path, json_path):

    document = Document(docx_path)

    #json 
    #提取file name, used for pics 
    file_name = os.path.basename(docx_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    # with open(json_path, 'r', encoding="utf-8") as file:
    #     json_data = json.load(file)

    data = {
        'indexCode':indexCode, 
        'postPerson':"", 
        'postText':"", 
        'postImg' :"", 
        'hasImg': False, 
        'commentPerson': "",
        'commentChoices': [],
        'otherComment':[ ]
    } 

    choice = {
        'index': 0,
        'choiceContent':"",
        'reply':{
            'person':"",
            'content':""
            }
    }

    speaker = ""
    content = ""
    # current_list = data["para"]
    isPost = True 

    for paragraph in document.paragraphs:
        line = paragraph.text.strip()
        print(line)

        if not line:
            continue

        if ":" in line:
            if speaker and content != "": #reached start of next dialogue 
                # print(speaker,content)
                if isPost: #朋友圈内容
                    data["postPerson"] = speaker
                    data["postText"] = content
                    isPost = False
                else: #评论内容
                    if speaker == "我": 
                        data["commentPerson"] = speaker
                        choice['choiceContent'] = content
                    elif "回复" in speaker: #查理苏回复我
                        choice['reply']['person'] = speaker.split("回复")[0]
                        choice['reply']['content'] = content
                        data['commentChoices'].append(choice)
                    else: #其他人回复
                        data['otherComment'].append({
                            'name': speaker,
                            'content' : content
                        })
                        

            speaker,choice_name = line.split(":")[0], line.split(":")[1]
            content = ""

            if speaker == "朋友圈内容":
                isPost = True

            elif speaker == "照片":
                if choice_name == "是":
                    data["hasImg"] = True
                    # 需要改照片名字和postImg
                    data["postImg"] = ""
                else:
                    data["hasImg"] = False
            
            # elif speaker == "评论内容":
            #     isPost = False

            elif speaker == "choice":
                choice = {
                    'index': int(choice_name),
                    'choiceContent':"",
                    'reply':{
                        'person':"",
                        'content':""
                    }
                }

        else: #continuous paragraph 
            content = line
            # print(speaker,content)
            
    if speaker and content != "": #end of doc
        if speaker == "我": 
            data["commentPerson"] = speaker
            choice['choiceContent'] = content
        elif "回复" in speaker: #查理苏回复我
            choice['reply']['person'] = speaker.split("回复")[0]
            choice['reply']['content'] = content
            data['commentChoices'].append(choice)
        else: #其他人回复
            data['otherComment'].append({
                'name': speaker,
                'content' : content
            })
            

    # json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    # print(data)
    subchap_data_list.append(data)

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(subchap_data_list, json_file, ensure_ascii=False, indent=4)

    return file_name_without_extension

    # print(json_data.decode('utf-8'))

    # return data

# 整合大章节信息
def extract_overview(docx_path, item, data):
    # print(docx_path)
    document = Document(docx_path)

    if item == '简介.docx': #简介
        
        for paragraph in document.paragraphs:
            line = paragraph.text.strip()

            if not line:
                continue

            if ":" in line:
                speaker, content = line.split(":")[0], line.split(":")[1]
                if speaker == "章节名":
                    data["name"] = content
                elif speaker == "简介":
                    data["intro"] = content
                else:
                    data["video"] = line
        

    else: #幕后
        sub_behind = { 
            "behind_name" : "",
            "content" : []
        }
        file_name_without_extension = os.path.splitext(item)[0]
        # print(file_name_without_extension)
        sub_behind["behind_name"] = file_name_without_extension

        for paragraph in document.paragraphs:
            line = paragraph.text.strip()
            sub_behind["content"].append(line)
        
        data["behind"].append(sub_behind)
        
        # with open(json_path, "w", encoding="utf-8") as json_file:
        #     json.dump(chap_data_list, json_file, ensure_ascii=False, indent=4)
        
    return data

def sort_by_integer(filename):
    # 使用正则表达式提取文件名中的整数部分
    match = re.match(r'(\d+)-', filename)
    if match:
        number = int(match.group(1))
        return number
    return 0  # 如果文件名不符合格式要求，则返回 0 进行排序


def main():
    os.chdir('./朋友圈')
                    

    doc_path = './10-第十章-装修新房.docx'  # 请将此路径替换为您的docx文件路径
    
    json_path = "10-第十章-装修新房.json"

    indexCode = "wm0001"
    extract_details(indexCode, doc_path, json_path)
    
    

if __name__ == '__main__':
    main()
