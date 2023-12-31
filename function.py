import csv

# 開啟 CSV 檔案



def init_data():
    global show_each_meal_dict
    global all_meal
    global info
    global re_info
    global all_order_meal_dict
    global list_view

    show_each_meal_dict = {}
    all_meal = []
    info = []
    all_order_meal_dict = {}
    re_info = []
    list_view = ''
    

    with open('meal.csv', newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)

        for row in rows:
            all_meal.append(row)
def check_exist(groupID):
    if not show_each_meal_dict.get(groupID): # 如果此群組為新加入，會創立一個新的儲存區
        show_each_meal_dict[groupID]={}
    if not all_order_meal_dict.get(groupID): # 如果此群組為新加入，會創立一個新的儲存區
        all_order_meal_dict[groupID]={}

def order(userName, groupID, receivedmsg):
    receivedmsg = receivedmsg.replace('!o','')

    re_info = get_meal_info(receivedmsg, userName, groupID)
    show_each_meal_dict[groupID][userName] = (re_info[0])


    table = tabular(show_each_meal_dict[groupID])

    print('個人明細: ', show_each_meal_dict[groupID])
    print('餐點數量: ', all_order_meal_dict[groupID])
    return table



def get_meal_info(receivedmsg, userName, groupID):
    # re_info = userName + ':'
    meal_list = receivedmsg.split()
    total = 0
    print(meal_list)
    info = []
    re_info = []
    total = 0

    for i in range(len(meal_list)):
        for j in range(len(all_meal)):
            if meal_list[i] == all_meal[j][0]:
                info.append(all_meal[j])

    for i in range(len(info)):     
        total += int(info[i][2]) #總金額

    for i in range(len(info)):
        re_info.append([info[i][1], info[i][2]])

    for i in range(len(meal_list)):
        if not all_order_meal_dict[groupID].get(info[i][1]): 
            all_order_meal_dict[groupID][info[i][1]] = 1
        else:
            all_order_meal_dict[groupID][info[i][1]] += 1

    return re_info, total

def tabular(show_each_meal_dict):   # 輸出可視化表格
    list_view = ''
    for i in show_each_meal_dict.keys():
        total = 0
        print(i)
        list_view += i + '\n'

        for key in show_each_meal_dict[i]:
            print(key)
            list_view += key[0] + ':\t' + key[1] + '\n'
            total += int(key[1])
        list_view += 'Total:\t\t' + str(total) + '\n\n'
    
    return list_view

def show_all(groupID):
    
    total = 0
    for i in range(len(all_order_meal_dict[groupID])):
        for j in range(len(all_meal)):
            if list(all_order_meal_dict[groupID].keys())[i] == all_meal[j][1]:
                total += int(all_meal[j][2])

    print(total)
    print(all_order_meal_dict)

    re_all = '明細:\n'

    for i in range(len(all_order_meal_dict[groupID])):
        re_all = re_all + str(list(all_order_meal_dict[groupID].keys())[i]) + str(list(all_order_meal_dict[groupID].values())[i]) + '份\n'
    re_all += '\n共 ' + str(total) + ' 元'
    return re_all


def msg_clear(groupID):
    all_order_meal_dict[groupID].clear()
    show_each_meal_dict[groupID].clear()
    tmp_str = '資料已重置!'
    return tmp_str

def delete(userName, groupID):

    for i in range(len(show_each_meal_dict[groupID][userName])):

        print(show_each_meal_dict[groupID][userName][i][0])
        all_order_meal_dict[groupID][show_each_meal_dict[groupID][userName][i][0]] -= 1

    del show_each_meal_dict[groupID][userName]
    print(show_each_meal_dict[groupID])

    return tabular(show_each_meal_dict[groupID])

def get_photo():
    message = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://imgur.com/gallery/CPPIeuV",
        "size": "full",
        "aspectRatio": "1:1",
        "action": {
        "type": "uri",
        "uri": "https://imgur.com/gallery/CPPIeuV"
        }
    }
    }
    return message

import requests

def post_help(groupID):
    # LINE Bot 的 Channel Access Token
    access_token = 'VbQ6iQgL+/jZEsEhrblBNmoKl/XBM9Vi+sjaACXAp4LD+vpQe1eiRP7ikBS0pHRy3d25YiBYgxdtF2js6s2sLR0VWYFU8O+sZzhy/Jzg1qXhJXCn32Q5am+kmQibsARrXpIelh88VYF5V8rz8309fAdB04t89/1O/w1cDnyilFU='

    # 要發送訊息的使用者ID
    user_id = str(groupID)  

    # 圖片的網址
    image_url = 'https://i.imgur.com/IoQALCm.png'  

    # 將訊息包裝成JSON格式
    message = {
        'to': user_id,
        'messages':[
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url
            }
        ]
    }

    # Set header
    headers = {'Authorization': 'Bearer ' + access_token}  

    # 發送POST請求到LINE Messaging API
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=message)

    # 打印回應
    print(response.text)

def post_res(groupID):
    # LINE Bot 的 Channel Access Token
    access_token = 'VbQ6iQgL+/jZEsEhrblBNmoKl/XBM9Vi+sjaACXAp4LD+vpQe1eiRP7ikBS0pHRy3d25YiBYgxdtF2js6s2sLR0VWYFU8O+sZzhy/Jzg1qXhJXCn32Q5am+kmQibsARrXpIelh88VYF5V8rz8309fAdB04t89/1O/w1cDnyilFU='

    # 要發送訊息的使用者ID
    user_id = str(groupID)  

    # 圖片的網址
    image_url = 'https://i.imgur.com/CXYiyFS.png'  

    # 將訊息包裝成JSON格式
    message = {
        'to': user_id,
        'messages':[
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url
            }
        ]
    }

    # Set header
    headers = {'Authorization': 'Bearer ' + access_token}  

    # 發送POST請求到LINE Messaging API
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=message)

    # 打印回應
    print(response.text)