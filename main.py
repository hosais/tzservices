from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    tzservices.run()
