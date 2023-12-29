from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage

)
from linebot.v3.messaging.models import FlexContainer as fl
from linebot.v3.messaging import TextMessage as tx

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os

# from linebot.models import FlexContainer

from func_db import *

app = Flask(__name__)

configuration = Configuration(access_token='VbQ6iQgL+/jZEsEhrblBNmoKl/XBM9Vi+sjaACXAp4LD+vpQe1eiRP7ikBS0pHRy3d25YiBYgxdtF2js6s2sLR0VWYFU8O+sZzhy/Jzg1qXhJXCn32Q5am+kmQibsARrXpIelh88VYF5V8rz8309fAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2e8e22c6ddca73678adfe875fc0c6b04')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
        
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        try:
            groupID = str(event.source.group_id)
            print(groupID)

        except: # 此機器人設計給群組回報，單兵不可直接一對一回報給機器人
            line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text='我只接收群組內訊息，請先把我邀請到群組!\n更多指令請打 !help')]
            )
        )
        
        else:
            userID = str(event.source.user_id)

            g_profile = line_bot_api.get_group_summary(groupID)
            groupName = g_profile.group_name

            u_profile = line_bot_api.get_group_member_profile(groupID,userID)
            userName = u_profile.display_name
            userName = str(userName)
            print(groupName, userName)

            check_exist(groupID)

            LineMessage = ''
            receivedmsg = event.message.text

            if '!o' in receivedmsg and len(receivedmsg)!=2:
                LineMessage = order(userName, groupID, receivedmsg)

            elif '!a' in receivedmsg and len(receivedmsg)==2:
                LineMessage = show_all(groupID)

            elif '!d' in receivedmsg and len(receivedmsg)==2:
                LineMessage = delete(userName, groupID)
            
            elif '!c' in receivedmsg and len(receivedmsg)==2:
                LineMessage = msg_clear(groupID)

            elif '!m' in receivedmsg and len(receivedmsg)!=2:
                LineMessage = cust(userName, groupID, receivedmsg)

            elif '!help' in receivedmsg and len(receivedmsg)==5:
                bubble_string = """{
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.imgur.com/8wSlvak.png",
    "size": "full",
    "aspectMode": "fit",
    "aspectRatio": "3:1.7"
  }
}"""
                message = FlexMessage(alt_text="使用說明", contents=fl.from_json(bubble_string))
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[message]
                    )
                )


            elif '!r' in receivedmsg and len(receivedmsg)==2:

                bubble_string = """{
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.imgur.com/f8X18tf.png",
    "size": "full",
    "aspectMode": "fit",
    "aspectRatio": "3:1.7",
    "action": {
      "type": "uri",
      "label": "action",
      "uri": "https://i.imgur.com/f8X18tf_d.webp?maxwidth=1520&fidelity=grand"
    }
  }
}"""
                message = FlexMessage(alt_text="菜單", contents=fl.from_json(bubble_string))
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[message]
                    )
                )

        if LineMessage :
            line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[tx(text=str(LineMessage))]
                )
            )
            
if __name__ == "__main__":
    init_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)