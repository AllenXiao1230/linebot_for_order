import requests

def post_help(groupID):
    # LINE Bot 的 Channel Access Token
    access_token = 'VbQ6iQgL+/jZEsEhrblBNmoKl/XBM9Vi+sjaACXAp4LD+vpQe1eiRP7ikBS0pHRy3d25YiBYgxdtF2js6s2sLR0VWYFU8O+sZzhy/Jzg1qXhJXCn32Q5am+kmQibsARrXpIelh88VYF5V8rz8309fAdB04t89/1O/w1cDnyilFU='

    # 要發送訊息的使用者ID
    user_id = str(groupID)  

    # 圖片的網址
    image_url = 'https://i.imgur.com/GQW926L.png'  

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
    image_url = 'https://i.imgur.com/GQW926L.png'  

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