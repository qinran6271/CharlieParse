import csv
from docx import Document
import os
import json
import re
import uuid

global subchap_data_list 
subchap_data_list  = []

global type_data_list
type_data_list = []

# 提炼小节文本
def extract_content(docx_path):

    document = Document(docx_path)

    #提取file name
    file_name = os.path.basename(docx_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    #
    unique_code = str(uuid.uuid4())
    indexCode = "ch"+ unique_code

    unique_code = str(uuid.uuid4())
    callCode = "v"+ unique_code

    # 创建append到overview data中的object
    overview_inner_data = {
            "dtype" : "", #聊天记录类型: calls-含视频通话, normal-普通聊天记录, voicemessage-含语音, redenvelope-含红包
            "name" : file_name_without_extension, #聊天记录名称
            "intro": "", #聊天记录简介内容
            "indexCode": indexCode #聊天记录索引值，ch开头
        }
    
    details_data = {
            "indexCode": indexCode, # 聊天记录索引值，ch开头
            "chatHistory": []
            }

    chatHistory = #相同说话人的内容都在一个obj里面 
    {
            "type": "nomarl", # normal无选项，choice有选项
            "speaker":"string", #说话人
            "content": [ # normal - text only
                {
                    "ifVoice": "boolean",#是否含有语音
                    "ifCall": "boolean",#是否含有通话
                    "ifImg": "boolean",#是否含有图片
                    "contentText": "string"#对话内容
                }
            ],
            "content": [ #has image - doesnt need "contentText"
                {
                "ifVoice": "boolean",
                "ifCall":"boolean",
                "ifImg": "boolean", # true
                "imgName" : "string",
                "imgPath": "string"# 当含有图片为真时显示的图片链接地址
                }
            ],
            "content": [ # call-plain text
                {
                    "ifVoice": "boolean", 
                    "ifCall":"boolean", # true
                    "ifImg": "boolean",
                    "imgName" : "string",
                    "call": {#当ifCall为真时返回的call内容
                        "title":"string",#聊天记录名称
                        "url":"string",#call链接地址
                        "callCode":"string"#call索引值,v开头
                    }
                }
            ],
            "content": [ #choice 我回复的选项
                {
                "ifVoice": "boolean",
                "ifCall":"boolean",
                "ifImg": "boolean",
                "contentText": "string",
                "imgPath": "string",# 当含有图片为真时显示的图片链接地址
                "reply": [
                    {
                        "replySpeaker" : "string", #回复人：我 or 查理苏
                        "ifVoice": "boolean",#是否含有语音
                        "ifImg": "boolean",#是否含有图片
                        "replyContent": "string",#对话内容
                        #如果有照片
                        "imgName" : "string",
                        "imgPath": "string"
                    }
                ]
                }
            ]
        }
    
    call_details = {
        "callCode":callCode, #call索引值,v开头
        "call_history" : []
    }


    speaker = ""
    content = []
    call_content = []
    current_list = data["para"]
    regular = True 
    call_url = ""
    if_call = False

    for paragraph in document.paragraphs:
        line = paragraph.text.strip()

        if not line:
            continue

        if ":" in line:
            if (speaker == "查理苏" or speaker == "我" )and content: #reached start of next dialogue 
                
                if if_call:
                    call_details["call_history"].append({
                        "speaker": speaker, #说话人名称
                        "content": call_content
                    })

                    call_content = []
 
                else:
                    if regular:
                        details_data["chatHistory"].append({
                            "type": "nomarl", # normal无选项，choice有选项
                            "speaker":speaker, #说话人
                            "content": content
                        })
                    else:
                        details_data["chatHistory"].append({
                            "type": "choice", # normal无选项，choice有选项
                            "speaker":speaker, #说话人
                            "content": content
                        })
                    content = []
            
            speaker,choice_name = line.split(":")[0], line.split(":")[1]

            if speaker == "类型": #call-含视频通话, normal-普通聊天记录, voicemessage-含语音, redenvelope-含红包
                if choice_name == "语音":
                    overview_inner_data["dtype"] = "voicemessage"
                elif choice_name == "普通":
                    overview_inner_data["dtype"] = "normal"
                elif choice_name == "红包":
                    overview_inner_data["dtype"] = "redenvelope"
                elif choice_name == "通话":
                    overview_inner_data["dtype"] = "call"

            elif speaker == "简介":
                overview_inner_data["intro"] = choice_name

            elif speaker == "https":
                call_url = line

            elif speaker == "区域开始":  
                regular = False

            elif speaker == "Choice":
                if_choice = True

            
        
            
            # 当前对话是语音
            elif speaker == "语音":
                data = {
                    "ifVoice": True,#是否含有语音
                    "ifCall": False,#是否含有通话
                    "ifImg": False,#是否含有图片
                    "contentText": choice_name#对话内容
                }
                content.append(data)
            
            elif speaker == "照片":
                data = {
                    "ifVoice": False,
                    "ifCall":False,
                    "ifImg":True, # true
                    "imgName" : choice_name,
                    "imgPath": choice_name + ".png"# 当含有图片为真时显示的图片链接地址 记得改
                }
                content.append(data)
            
            elif speaker == "通话开始":
                data = {
                    "ifVoice": False, 
                    "ifCall":True, # true
                    "ifImg":False,
                    "call": {#当ifCall为真时返回的call内容
                        "title": file_name_without_extension,#聊天记录名称
                        "url": call_url,#call链接地址
                        "callCode": callCode#call索引值,v开头
                    }
                }

                content.append(data)
                if_call = True

        


            
        elif "区域结束" in line:
            regular = True    

        elif "通话结束" in line:
            if_call = False

        # 普通 or 通话
        else:
            if if_call:
                data = {
                    "contentText" : line
                }
                call_content.append(data)
                

            else:
                data = {
                    "ifVoice": False,#是否含有语音
                    "ifCall": False,#是否含有通话
                    "ifImg": False,#是否含有图片
                    "contentText": line #对话内容
                }
                content.append(data)
            

           
            
               
       
            
    if speaker and content: #end of doc
        if regular:
            current_list.append({
                "para_type": "normal",
                "speaker": speaker,
                "content": content,
                "tag": tag
            })    
        else:
            current_list.append({
                "speaker": speaker,
                "content": content,
                "tag": tag
            })    

    # json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    subchap_data_list.append(data)

    # with open(json_path, "w", encoding="utf-8") as json_file:
    #     json.dump(subchap_data_list, json_file, ensure_ascii=False, indent=4)

    return overview_inner_data

    # print(json_data.decode('utf-8'))

    # return data


   

def sort_by_integer(filename):
    # 使用正则表达式提取文件名中的整数部分
    match = re.match(r'(\d+)-', filename)
    if match:
        number = int(match.group(1))
        return number
    return 10000  # 如果文件名不符合格式要求，则返回 0 进行排序

def main():
    os.chdir('./聊天记录/聊天记录文本') #mark data as root dir

    # types = sorted(os.listdir(),key=sort_by_integer) #find all subdirs / chapters & sort
    types = os.listdir()
    # print(types)
    for type_name in types: 
        type_path = './' + type_name
        # "照片" 记得改
        if type_name == "照片":
            continue

        # 替换成英语名称
        elif type_name == "灵犀":
            type_name = "lingXi"
        elif type_name == "邂逅":
            type_name = "xieHou"
        elif type_name == "活动":
            type_name = "activities"
        elif type_name == "真话冒险":
            type_name = "truthorDare"
        elif type_name == "茶歇":
            type_name = "teaParty"   
        else:
            type_name = "mainStory"  

        #创建返回data
        para_type_data = {
                "totalNum" : 0, #某一个type聊天记录的总数
                "type" : type_name, #lingXi（灵犀）、xieHou（邂逅）、activities（活动）、truthorDare（真话冒险）、teaParty（茶歇）、mainStory（主线）
                "data" : []
                }
        print(type_name)
        # subchap_nums = [] # 储存当前所有小节的编号
        # ending= []

        type_list = os.listdir(type_path)

        # 填充type聊天记录的总数
        para_type_data["totalNum"] = len(type_list)
        json_path = "../overview.json"

        for item in type_list: #每章节里面的所有文档/文件夹
            sub_path = os.path.join(type_path, item) # sub_path 是每个type里面文件的路径
            para_type_data["data"].append(extract_content(sub_path))


        # 生成大章节json文件
        type_data_list.append(para_type_data)
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(type_data_list, json_file, ensure_ascii=False, indent=4)

                    

    # filename = './主线文本/7-13'  # 请将此路径替换为您的docx文件路径
    # docx_path = filename + '.docx'
    
    # json_path = "test" + ".json"
    # extract_content(docx_path, json_path)
    
    

if __name__ == '__main__':
    main()
