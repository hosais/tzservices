# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com



from tzm import tzbot

from flask import Flask, render_template

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

tzservices = Flask(__name__)
idf = open("id.txt")
idf.readline().rstrip()  # remove newline (ignore first line)
idf.readline().rstrip()  # remove newline (ignore second line)
tzservices.config["SECRET_KEY"] = idf.readline().rstrip()
idf.close()

bcrypt = Bcrypt(tzservices)
login_manager = LoginManager(tzservices)
login_manager.login_view = "login_page"
# redirect to login page when accssing login required pages, if user not Login    
login_manager.login_message_category = "info"
# this related to style of the message showed on web

from tzm import routes
