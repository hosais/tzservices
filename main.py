# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com


from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort
import os
import sys
import copy
import inputimeout
import tzdb
import json


sys.path.insert(0, os.path.dirname(__file__))


tzservices = Flask(__name__)

idf = open("id.txt")
YOUR_CHANNEL_ACCESS_TOKEN = idf.readline().rstrip()  # remove newline
YOUR_CHANNEL_SECRET = idf.readline().rstrip()  # remove newline
# YOUR_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(
    YOUR_CHANNEL_ACCESS_TOKEN)

# YOUR_CHANNEL_SECRET
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


# 333
# flex message template
flex_bubble_template = {
    "type": "bubble",
    "hero": {
            "type": "image",
            "url": "https://www.tarozafra.com/assets/images/santiago.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://www.tarozafra.com/"
            }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Santiago Cake",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Ingredient",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "Almond",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Price",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "$120",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "I want",
                    "text": "I would like to have Santiago cake. "
                }
            },
            {
                "type": "button",
                "style": "secondary",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "Cart",
                    "text": "Tell me what I ordered currently"
                }
            },

        ],
    }
}


def make_menu():
    flex_message_json = {
        "type": "carousel",
        "contents": []
    }
    items = [
        {
            "name": "Santiago Cake",
            "image_url": "https://www.tarozafra.com/assets/images/santiago.jpg",
            "price": 80,
            "Ingredients": "ingredients text",
        },
        {
            "name": "Apple Cake",
            "image_url": "https://www.tarozafra.com/assets/images/santiago.jpg",
            "price": 90,
            "Ingredients": "ingredients text 65%%  apple",
        }

    ]
    for item in items:
        flex_bubble = copy.deepcopy(flex_bubble_template)
        flex_bubble["hero"]["url"] = item["image_url"]
        flex_bubble["body"]["contents"][0]["text"] = item["name"]
        flex_bubble["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = "$" + \
            str(item["price"])
        flex_bubble["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = item["Ingredients"]
        flex_message_json["contents"].append(flex_bubble)

    return flex_message_json


lbme_db = tzdb.linebot_msg_event()


@tzservices.route('/')
def hello_world():
    return 'Hello, World!'


@tzservices.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    tzservices.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# event structure
event_template = {
    "message":  {"id": "14339762965727", "text": "I would like to have Santiago cake. ", "type": "text"},
    "mode": "active",
    "replyToken": "90283169cf71442eaa46c0f3905a3c7b",
    "source": {"type": "user", "userId": "U8c0f51197c2eb9ec822878cbc35c451c"},
    "timestamp": 1625462823884, "type": "message"
}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info
    # print(event.source)

    profile = line_bot_api.get_profile(
        event.source.user_id)  # user_id instead of userId

    # refer to https://github.com/line/line-bot-sdk-python/blob/master/linebot/models/events.py
    # https://github.com/line/line-bot-sdk-python/blob/764c1b40c09f6e203a07799161117ce64d3574a7/linebot/models/base.py#L120
    # you can interchange from dict to line object from its functions defined in base.py
    event_dict = event.as_json_dict()
    event_dict["profile"] = profile.as_json_dict()
    lbme_db.save_msg_event(event_dict)

    # print("userinfo:")
    #print("display_name: "+profile.display_name)
    # print("user_id: "+profile.user_id)  # user_id instead of userId
    #print("picture_url: "+profile.picture_url)

    flex_message_json = make_menu()
    if event.message.type == "text":
        if event.message.text == "I would like to have Santiago cake. ":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="您要幾片(請只回答數字)?")
            )
        else:
            flex_message = FlexSendMessage(
                alt_text='hello',
                contents=flex_message_json
            )
            line_bot_api.reply_message(
                event.reply_token,
                flex_message
            )


if __name__ == "__main__":
    tzservices.run()
