import csv
from docx import Document
import os
import json
import re
import uuid

global details_data_list 
details_data_list  = []

global type_data_list
type_data_list = []

global call_data_list
call_data_list = []

# 提炼小节文本
def extract_content(docx_path,type):

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
    if 'lingXi' == type or 'xieHou'== type:
                overview_inner_data["name"] = file_name_without_extension[1:]
    
    details_data = {
            "indexCode": indexCode, # 聊天记录索引值，ch开头
            "chatHistory": []
            }

    
    
    call_details = {
        "callCode":callCode, #call索引值,v开头
        "call_history" : []
    }


    speaker = ""
    person = ""
    content = []
    call_content = []
    choice_content = []
    regular = True 
    call_url = ""
    caller = ""
    if_call = False
    if_choice = False
    if_reply = False
    choice_obj = {}
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
            if ("查理苏:" in line or "我:" in line or "区域开始:" in line) and content: #reached start of next dialogue 
                
                if if_call:
                    
                    if caller == "":
                        caller = person

                    if call_content != []:
                        call_details["call_history"].append({
                            "speaker": person, #说话人名称
                            "content": call_content
                        })
                        call_content = []

                elif if_choice and not if_reply:
                    choice_obj = content[0]
                    choice_obj["reply"] = []
                    if_reply = True
                    content = []
    
                elif regular:
                    details_data["chatHistory"].append({
                        "type": "nomarl", # normal无选项，choice有选项
                        "speaker":person, #说话人
                        "content": content
                    })
                    content = []
            

            if "查理苏:" in line:
                person = "查理苏"
            elif "我:" in line:
                person = "我"
            # else:
            #     if not if_reply:
            #         person = ""

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
                overview_inner_data["intro"] = line[3:]

            elif speaker == "https":
                call_url = line

            # elif speaker == "区域开始":  
            #     print(person,content)
            #     regular = False

            elif speaker == "Choice":
                regular = False
                if_choice = True
                if_reply = False
                if int(choice_name) > 1:
                    choice_content.append(choice_obj)

            
        
            
            # 当前对话是语音
            elif speaker == "语音":
                if if_reply:
                    data = {
                        "ifVoice": True,#是否含有语音
                        "ifCall": False,#是否含有通话
                        "ifImg": False,#是否含有图片
                        "contentText": choice_name, #对话内容
                        "replySpeaker" : person
                    }
                    choice_obj["reply"].append(data)
                else:
                    data = {
                        "ifVoice": True,#是否含有语音
                        "ifCall": False,#是否含有通话
                        "ifImg": False,#是否含有图片
                        "contentText": choice_name#对话内容
                    }
                    content.append(data)
            
            elif speaker == "照片":
                # 因为现在所有照片都是png格式，所以写死了。如果以后有jpg格式，记得修改（可以参考朋友圈）
                if if_reply:
                    data = {
                        "ifVoice": False,
                        "ifCall":False,
                        "ifImg":True, # true
                        "imgPath": "https://charlie-backend.oss-cn-hongkong.aliyuncs.com/chat-history/"+choice_name + ".png",# 当含有图片为真时显示的图片链接地址
                        "replySpeaker" : person
                    }
                    choice_obj["reply"].append(data)
                else:
                    data = {
                        "ifVoice": False,
                        "ifCall":False,
                        "ifImg":True, # true
                        "imgPath": "https://charlie-backend.oss-cn-hongkong.aliyuncs.com/chat-history/"+choice_name + ".png"# 当含有图片为真时显示的图片链接地址
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
            if_choice = False
            if_reply = False
            regular = True  
            choice_content.append(choice_obj)
            details_data["chatHistory"].append({
                "type": "choice",
                "speaker": "我", #说话人名称
                "content": choice_content
            })
            choice_content = []  
            choice_obj = {}


        elif "通话结束" in line:
            call_details["call_history"].append({
                            "speaker": person, #说话人名称
                            "content": call_content
                        })
            call_content = []

            details_data["chatHistory"].append({
                        "type": "nomarl", # normal无选项，choice有选项
                        "speaker":caller, 
                        "content": content
                    })
            content = []
            if_call = False


        # 普通 or 通话
        else:
            if if_call:
                data = {
                    "contentText" : line
                }
                call_content.append(data)
                
            elif if_reply:
                data = {
                    "ifVoice": False,#是否含有语音
                    "ifCall": False,#是否含有通话
                    "ifImg": False,#是否含有图片
                    "contentText": line, #对话内容
                    "replySpeaker" : person
                }
                choice_obj["reply"].append(data)
            else:
                data = {
                    "ifVoice": False,#是否含有语音
                    "ifCall": False,#是否含有通话
                    "ifImg": False,#是否含有图片
                    "contentText": line #对话内容
                }
                content.append(data)
            

            
    if person and content:
                
        if if_call:
            call_details["call_history"].append({
                "speaker": person, #说话人名称
                "content": call_content
            })

            call_content = []

        elif if_choice and not if_reply:
            choice_obj = content[0]
            choice_obj["reply"] = []
            if_reply = True
            content = []

        elif regular:
            details_data["chatHistory"].append({
                "type": "nomarl", # normal无选项，choice有选项
                "speaker":person, #说话人
                "content": content
            })
            content = []


    details_data_list.append(details_data)
    deatils_json = "../details.json"

    if call_url != "":
        call_data_list.append(call_details)
    calls_json = "../calls.json"

    with open(deatils_json, "w", encoding="utf-8") as json_file:
        json.dump(details_data_list, json_file, ensure_ascii=False, indent=4)

    with open(calls_json, "w", encoding="utf-8") as json_file:
        json.dump(call_data_list, json_file, ensure_ascii=False, indent=4)

    return overview_inner_data



   

def sort_by_integer(filename):
    match = re.search(r'(\d+(\.\d+)?)', filename)
    if match:
        number = float(match.group(1))
        return number
    return 0.0  # 如果文件名不符合格式要求，则返回 0 进行排序

def main():
    os.chdir('./聊天记录/聊天记录文本新') #mark data as root dir

    # types = sorted(os.listdir(),key=sort_by_integer) #find all subdirs / chapters & sort
    types = os.listdir()
    # print(types)
    for type_name in types: 
        type_path = './' + type_name

        # "照片" 记得改
        # if type_name == "照片":
        #     continue

        # 替换成英语名称
        if type_name == "灵犀":
            type_name = "lingXi"
        elif type_name == "邂逅":
            type_name = "xieHou"
        elif type_name == "活动":
            type_name = "activities"
        elif type_name == "真心话大冒险":
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

        type_list = sorted(os.listdir(type_path),key=sort_by_integer)
        print(type_list)
        # type_list = os.listdir(type_path)

        # 填充type聊天记录的总数
        para_type_data["totalNum"] = len(type_list)
        json_path = "../overview.json"

        for item in type_list: #每章节里面的所有文档/文件夹
            sub_path = os.path.join(type_path, item) # sub_path 是每个type里面文件的路径
            para_type_data["data"].append(extract_content(sub_path,type_name))


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
