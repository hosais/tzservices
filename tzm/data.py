# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com


from tzm.tzdb import DbDataCo, mdb
from tzm import bcrypt
from pymongo import IndexModel, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from tzm.base import print_error
from flask_login import UserMixin
from tzm import login_manager


# menually keyinjson format for menu
# create validator
# price calculator validator for input string (product name)
# item1 item2 item3 base1 + addon_productx1  -> price


if __name__ == "__main__":
    try:
        pass

    except Exception as e:
        print_error(e)

else:
    pass
    # open database configruation by default value

    # collection linebot msg events
