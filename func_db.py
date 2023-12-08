import csv

import sqlite3

import requests

def init_data():   


    global all_meal
    global info
    global re_info
    global list_view

    all_meal = []
    info = []
    re_info = []
    list_view = '' 

    with open('meal.csv', newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)

        for row in rows:
            all_meal.append(row)

con = sqlite3.connect('order_database.db', check_same_thread=False)
cur = con.cursor()
          
def check_exist(groupID):
    
    cur.execute(f'CREATE TABLE IF NOT EXISTS {groupID}(userName, order_item, price)')
    con.commit()

    cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Allen', 'itemA', 10))
    cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Ian', 'itemB', 20))
    cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Ryan', 'itemC', 50))
    cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Vivi', 'itemA', 10))
    cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Bob', 'itemB', 20))
    con.commit()

def order(userName, groupID, receivedmsg):
    receivedmsg = receivedmsg.replace('!o','')

    re_info = get_meal_info(receivedmsg, userName, groupID)
    #show_each_meal_dict[groupID][userName] = (re_info)

    for i in len(re_info):
        cur.execute(f"INSERT INTO {groupID} VALUES(?, ?, ?)", (userName, re_info[i][0], re_info[i][1]))
        con.commit()

    table = tabular(groupID, userName)

    return table



def get_meal_info(receivedmsg, userName, groupID):
    # re_info = userName + ':'
    meal_list = receivedmsg.split()
    total = 0
    info = []
    re_info = []

    for i in range(len(meal_list)):    #from code get meal name
        for j in range(len(all_meal)):
            if meal_list[i] == all_meal[j][0]:
                info.append(all_meal[j])

    for i in range(len(info)):
        re_info.append([info[i][1], info[i][2]])

    return re_info

def tabular(groupID):   # 輸出可視化表格
    
    list_view = ''
    
    for i in cur.execute(f"SELECT userName FROM {groupID}'"):
        
        total = 0
        ret = cur.execute(f"SELECT order_item, price FROM {groupID} WHERE userName='{i}'")
        
        if list_view == '':
            list_view += i + '\n'
            for key in ret:
                list_view += key[0] + ':\t' + key[1] + '\n'
                total += int(key[1])
            list_view += 'Total:\t\t' + str(total)
            
        else:
            list_view += '\n\n' + i + '\n'
            for key in ret:
                list_view += key[0] + ':\t' + key[1] + '\n'
                total += int(key[1])
            list_view += 'Total:\t\t' + str(total)

    return list_view

def show_all(groupID):
    
    total = 0
    total = str(list(cur.execute(f'SELECT SUM (price) FROM {groupID}'))[0][0])

    all_list = list(cur.execute(f'SELECT order_item as items,COUNT(*) as times FROM {groupID} GROUP BY order_item'))


    print(total)
    print(list(all_list))

    re_all = '明細:\n'

    for i in all_list:
        re_all = re_all + str(i[0]) + str(i[1]) + '份\n'

    re_all += '\n共 ' + str(total) + ' 元'
    return re_all


def msg_clear(groupID):
    cur.execute(f'DELETE FROM {groupID}')
    tmp_str = '資料已重置!'
    return tmp_str

def delete(userName, groupID):

    cur.execute(f'DELETE FROM {groupID} WHERE userName = {userName}')

    # for i in range(len(show_each_meal_dict[groupID][userName])):

    #     print(show_each_meal_dict[groupID][userName][i][0])
    #     all_order_meal_dict[groupID][show_each_meal_dict[groupID][userName][i][0]] -= 1

    # del show_each_meal_dict[groupID][userName]
    # print(show_each_meal_dict[groupID])

    return tabular(groupID)

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
