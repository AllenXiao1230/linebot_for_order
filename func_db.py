import csv

import sqlite3

import requests

from linebot.models import *
# from linebot.models import *

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

    # cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Allen', 'itemA', 10))
    # cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Ian', 'itemB', 20))
    # cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Ryan', 'itemC', 50))
    # cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Vivi', 'itemA', 10))
    # cur.execute(f'INSERT INTO {groupID} VALUES (?, ?, ?)', ('Bob', 'itemB', 20))
    # con.commit()

def order(userName, groupID, receivedmsg):
    delete(userName, groupID)
    receivedmsg = receivedmsg.replace('!o','')
    receivedmsg = receivedmsg.upper()
    
    re_info = get_meal_info(receivedmsg, userName, groupID)

    print(re_info)

    if len(re_info) == 0:
        return '請輸入正確的餐點'
    
    for i in re_info:
        cur.execute(f"INSERT INTO {groupID} VALUES(?, ?, ?)", (userName, i[0], i[1]))
        con.commit()

    table = tabular(groupID)

    return table

def cust(userName, groupID,  receivedmsg):

    info = []
    re_info = []

    delete(userName, groupID)
    receivedmsg = receivedmsg.replace('!m','')
    receivedmsg = receivedmsg.split(',')

    for i in receivedmsg:
        re_info.append([i.split()[0], i.split()[1]])

    print(re_info)

    if len(re_info) == 0:
        return '請輸入正確的餐點'
    
    for i in re_info:
        cur.execute(f"INSERT INTO {groupID} VALUES(?, ?, ?)", (userName, i[0], i[1]))
        con.commit()

    table = tabular(groupID)

    return table



def get_meal_info(receivedmsg, userName, groupID):
    # re_info = userName + ':'
    meal_list = receivedmsg.split()
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
    
    for i in cur.execute(f"SELECT userName FROM {groupID}"):
        
        total = 0
        ret = cur.execute(f"SELECT order_item, price FROM {groupID} WHERE userName=?",(i))
        
        if list_view == '':
            list_view += str(i[0]) + '\n'
            for key in ret:
                list_view += key[0] + ':\t' + key[1] + '\n'
                total += int(key[1])
            list_view += 'Total:\t\t' + str(total)
            
        else:
            list_view += '\n\n' + str(i[0]) + '\n'
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

    if re_all == '':
        return '目前無人點餐'
    else:
        msg_clear()
        return re_all


def msg_clear(groupID):
    cur.execute(f'DELETE FROM {groupID}')
    con.commit()
    tmp_str = '資料已重置!'
    return tmp_str

def delete(userName, groupID):

    cur.execute(f'DELETE FROM {groupID} WHERE userName="{userName}"')
    con.commit()

    return tabular(groupID)
