from docx import Document
import os
import json
import re

global subchap_data_list 
subchap_data_list  = []

global card_data_list
card_data_list = []

# 提炼小节文本
def extract_content(card_name, total_num, docx_path):

    document = Document(docx_path)

    #提取file name
    file_name = os.path.basename(docx_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    file_elem = file_name_without_extension.split('-')

    data = {
        "card_name" : card_name, 
        "chap_num" : int(file_elem[0]), #小节数
        "chap_name" : file_elem[1], #小节名
        "total_num" : total_num, #小节总数
        "part" : file_elem[2] if len(file_elem) > 2 else "", #罗马数字
        "video" : "", #视频链接
        "para" : []
    }


    speaker = ""
    content = ""
    current_list = data["para"]

    paragraphs = [] 
    
    for paragraph in document.paragraphs:
        text_parts = paragraph.text.split('\n')
        # print(text_parts)
        for text_part in text_parts:
                # 忽略空文本部分
            paragraphs.append(text_part.strip())

    for line in paragraphs:

        if not line:
            continue

        if ":" in line:
            if speaker and content: #reached start of next dialogue 
                current_list.append({
                    "speaker": speaker,
                    "content": content,
                    "tag": tag
                })
                
            
            speaker = line.split(":")[0]
            content = ""
            tag = ""

            if speaker == "视频链接":
                data["video"] = line[5:].strip()
            #处理 tag 
            elif speaker == "查理苏":
                tag = "charlie"
            elif speaker == "我":
                tag = "me"
            elif speaker == "旁白":
                tag = "pb"
            else:
                tag = "others"


        else: #continuous paragraph 
            content += line + '\n'
            
    if speaker and content: #end of doc
        current_list.append({
            "speaker": speaker,
            "content": content,
            "tag": tag
        }) 

    # json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    subchap_data_list.append(data)

    with open("../film_chaps.json", "w", encoding="utf-8") as json_file:
        json.dump(subchap_data_list, json_file, ensure_ascii=False, indent=4)

    return file_name_without_extension


def sort_by_integer(filename):
    # 使用正则表达式提取文件名中的整数部分
    match = re.match(r'(\d+)-', filename)
    if match:
        number = int(match.group(1))
        return number
    return 10000  # 如果文件名不符合格式要求，则返回 0 进行排序

def main():
    os.chdir('./记忆-胶片/胶片文本') #mark data as root dir

    cards = os.listdir()

    for card in cards: 
        
        card_path = './' + card

        chapters = sorted(os.listdir(card_path),key=sort_by_integer) #给小节排序

        data = {
            "card_name" : card, 
            "total_num" : len(chapters), #小节总数
            "chaps" : [os.path.splitext(name)[0] for name in chapters] #小节
        }

        for item in os.listdir(card_path): #每张卡里面的所有文档
            cur_path = os.path.join(card_path, item) 

            extract_content(card, len(chapters), cur_path)

        json_path = "../film_cards.json"
        # 生成大章节json文件
        card_data_list.append(data)
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(card_data_list, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
