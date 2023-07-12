from docx import Document
import os
import json

global data_list 
data_list  = []


# 提炼文本
def extract_details(docx_path, json_path):

    document = Document(docx_path)

    file_name = os.path.basename(docx_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    data = {
        "id" : 0,
        "card" : "",
        "more" : ""
    }

    for paragraph in document.paragraphs:
        line = paragraph.text.strip()
        print(line)

        if not line:
            continue

        if "-" in line:
            elements = line.split("-")
            data["id"] = int(elements[0])
            data["card"] = elements[1].strip()
            data["more"] = elements[2].strip()

            data_list.append(data)

            data = {
                "id" : 0,
                "card" : "",
                "more" : ""
            } 

    
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    return file_name_without_extension


def main():
    os.chdir('./关于charlie')

    extract_details("./细节sample.docx","./角色细节.json")

    


if __name__ == '__main__':
    main()
