# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com



from tzm import tzbot

from flask import Flask, render_template
from tzm.tzdb import linebot_msg_event

tzservices = Flask(__name__)

lbme_db = linebot_msg_event()

from tzm import routes

