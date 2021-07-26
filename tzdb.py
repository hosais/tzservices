# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
import pymongo
import json
import pprint


class Mdb:
    def __init__(self, db_info_file="db_info.json") -> None:
        # setup mongodb server
        self.db_info = self.load_db_info(db_info_file)
        self.db_client = pymongo.MongoClient(
            "mongodb+srv://"
            + self.db_info["db_user"]+":"+self.db_info["db_pw"]
            + "@"+self.db_info["db_host_DN"]
            + "/"+self.db_info["db_name"]
            + "?retryWrites=true&w=majority")
        self.db = self.db_client.tzdb

    def load_db_info(self, db_info_file):
        db_info_f = open(db_info_file)
        db_info_content = db_info_f.read()
        db_info = json.loads(db_info_content)
        return db_info


class linebot_msg_event(Mdb):
    '''
    event_template = {
        "message":  {"id": "14339762965727", "text": "I would like to have Santiago cake. ", "type": "text"},
        "mode": "active",
        "replyToken": "90283169cf71442eaa46c0f3905a3c7b",
        "source": {"type": "user", "userId": "U8c0f51197c2eb9ec822878cbc35c451c"},
        "timestamp": 1625462823884, "type": "message"
    }
    '''

    def __init__(self, db_info_file="db_info.json"):
        super().__init__(db_info_file)
        # collection of msg_events
        self.msg_events_col = self.db.linebot_msgs

    def save_msg_event(self, event, extra_info=None):
        if extra_info != None:
            event["Extra_info"] = extra_info
        self.msg_events_col.insert_one(event)

    def find_event_with_userid(self, userid):
        '''
        return found records
        '''
        return msgs_dbcol.find(
            {
                "source.userId": userid,
            }
        )


if __name__ == "__main__":
    try:
        tzdb = Mdb()
        client = tzdb.db_client
        # client= pymongo.MongoClient(
        #   "mongodb+srv://tzmongo:pymonjoe1@tzcluster.fp5yu.mongodb.net/tzdb?retryWrites=true&w=majority")
        print("show database: ")
        print(client.list_database_names())
        tzdb = client.tzdb
        print(tzdb)
        msgs_dbcol = tzdb.linebot_msgs
        linebot_msgevent = {
            "message":  {"id": "14339762965727", "text": "I would like to have Santiago cake. ", "type": "text"},
            "source": {"type": "user2", "userId": "U8c0f51197c2eb9ec822878cbc35c451c"},
            "timestamp": 1625462823884,
            "type": "message"
        }
        print("before insert")
        # msgs_dbcol.insert_one(linebot_msgevent)
        print(tzdb.list_collection_names())
        print("before find")
        # pprint.pprint(msgs_dbcol.find_one())
        msg_events = msgs_dbcol.find(
            {
                "source.userId": "U8c0f51197c2eb9ec822878cbc35c451c",
            }
        )
        for msg_event in msg_events:
            pprint.pprint(msg_event)

    except Exception as e:
        print("An exception occurred ::", e)
