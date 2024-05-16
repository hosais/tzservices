# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com

from tzm.tzdb import mdb
from tzm.tzdb import user_cl
from tzm import bcrypt


class User:
    db = mdb
    col = mdb.get_db()["user"]

    def __init__(self, **kwarg) -> None:
        for key, value in kwarg.items():
            setattr(self, key, value)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    @classmethod
    def find_by_username(cls, username, one=True):
        if one:
            user_dict = cls.col.find_one({"username": username})
            if user_dict != None:
                return cls(user_dict)
            else:
                return None
        else:
            print("warnning: NOT implemented yet. Unpredictable result effect")
            return cls.col.find({"username": username})

    @classmethod
    def find_by_email(cls, email_address, one=True):
        if one:
            user_dict = cls.col.find_one({"email_address": email_address})
            if user_dict:
                return cls(user_dict)
            else:
                return None
        else:
            print("warnning: NOT implemented yet. Unpredictable result effect")
            return cls.col.find({"email_address": email_address})
