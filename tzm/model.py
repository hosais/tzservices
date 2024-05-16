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


################################################################3
############### USER Model #################################3
###########################################################


@login_manager.user_loader
def load_user(user_id):
    """
    This will load User to the html template variable
    """
    user_dict = User.col.find_one({"_id": ObjectId(user_id)})
    if user_dict == None:
        print("warning!! user_dict should not be None(Not Found a user)")
    return User(user_dict)


class User(DbDataCo, UserMixin):
    ################### begin col ##########################################33
    # __qualname__ == class name and will NOT inherit from base class => every datacomponent child needs to have these two lines
    col_name = __qualname__
    col = mdb.get_db()[__qualname__]
    #################### end col ############################################
    # model fields can be check and accessed if needed by self.model_fields but it is readonly

    _model_fields = {
        #'_id':'',     handled by nmongodb
        "username": "joseph",  # line display name
        "lineID": "user_lineid",
        "email_address": "default@hotmail.com",
        "password_hash": "xxx",
        "cart_total": 1000,  # <- need to change in the future
        "orders": [],
    }

    _db_index_list = [
        IndexModel([("username", DESCENDING)], unique=True),
        IndexModel([("email_address", DESCENDING)], unique=True),
        IndexModel([("lineID", DESCENDING)], unique=True, sparse=True),
    ]

    def __init__(self, dict_obj=None, isCopy=True):
        try:
            # get default data from _model_fields  (self.data = _model_fields)
            super(User, self).__init__(dict_obj, isCopy)
            # do customized thing here

        except Exception as e:
            print_error(e)

    @property
    def password(self):
        return self.getField("password_hash")

    @password.setter
    def password(self, plain_text_password):
        self.setField(
            "password_hash",
            bcrypt.generate_password_hash(plain_text_password).decode("utf-8"),
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(
            self.getField("password_hash"), attempted_password
        )

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
            return cls(cls.col.find({"username": username}))

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
            return cls(cls.col.find({"email_address": email_address}))

    @classmethod
    def find_event_with_userid(cls, userid):
        """
        !!! need to move to linebot_msgs class
        only for linebot_msgs collection
        return found records
        """
        return cls(
            cls.col.find(
                {
                    "source.userId": userid,
                }
            )
        )

    def delete_user(self):
        """
        !!! need to move to linebot_msgs class
        only for linebot_msgs collection
        return found records
        """
        return type(self).col.delete_one(
            {
                "username": self.data["username"],
            }
        )


################################################################3
############### MenuModifier Model #################################3
###########################################################
class MenuModifier(DbDataCo):
    pass


if __name__ == "__main__":
    try:
        user_dic = {
            #'_id':'',     handled by nmongodb
            "username": "joseph",  # line display name
            "lineID": "user_lineid",
            "email_address": "default@hotmail.com",
            "password_hash": "xxx",
            "cart_total": 1000,
            "orders": [],
        }
        user_dic2 = {
            #'_id':'',     handled by nmongodb
            "username": "jose123ph",  # line display name
            "lineID": "user_li123neid",
            "email_address": "de123fault@hotmail.com",
            "password_hash": "xx213x",
            "cart_total": 10020,
            "orders": [],
        }
        t1 = User(user_dic)
        t2 = User(user_dic2)
        t1.insert_doc()
        t2.insert_doc()

        result = User.find_by_username("joseph")
        result.printDataObj()
        # result = t1.delete_user()
        # print(f"{result.deleted_count} deleted")
        # result = t2.delete_user()
        # print(f"{result.deleted_count} deleted")

    except Exception as e:
        print_error(e)
