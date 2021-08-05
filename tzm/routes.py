# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
from flask import Flask, request, abort
from flask import render_template

from tzm import tzservices


@tzservices.route('/')
def home_page():
    print("err")
    return render_template('home.html')

@tzservices.route('/order')
def order_page():    
    return render_template('order.html')

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
