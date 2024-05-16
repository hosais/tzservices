# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
import pymongo
from pymongo import IndexModel, ASCENDING, DESCENDING
import json
import pprint
import copy
from tzm.base import print_error
from bson import ObjectId


class Mdb:
    def __init__(self, db_info_file="db_info.json") -> None:
        # setup mongodb server
        self.db_info = self.load_db_info(db_info_file)
        # client= pymongo.MongoClient(
        #   "mongodb+srv://tzmongo:pymonjoe1@tzcluster.fp5yu.mongodb.net/tzdb?retryWrites=true&w=majority")
        # f' format
        # message = (
        # ...         f"Hi {name}. "
        # ...         f"You are a {profession}. "
        # ...         f"You were in {affiliation}."
        #    ... )
        connect_str = (
            f"mongodb+srv://"
            f"{self.db_info['db_user']}"
            f":"
            f"{self.db_info['db_pw']}"
            f"@"
            f"{self.db_info['db_host_DN']}"
            f"/"
            f"{self.db_info['db_name']}"
            f"?retryWrites=true&w=majority"
        )

        # temporally use fixed datbase string !!!!!!!!!!  use python version 3.4 or later
        conneect_str34 = "mongodb://tzmongo:pymonjoe1@tzcluster-shard-00-00.fp5yu.mongodb.net:27017,tzcluster-shard-00-01.fp5yu.mongodb.net:27017,tzcluster-shard-00-02.fp5yu.mongodb.net:27017/?ssl=true&replicaSet=atlas-ajnnj9-shard-0&authSource=admin&retryWrites=true&w=majority"
        print(
            "temporally use fixed datbase connection string !!!!!!!!!!  use python version 3.4 or later"
        )
        self.db_client = pymongo.MongoClient(conneect_str34)

        self.mongodb = self.db_client[self.db_info["db_name"]]

    def load_db_info(self, db_info_file):
        db_info_f = open(db_info_file)
        db_info_content = db_info_f.read()
        db_info = json.loads(db_info_content)
        return db_info

    def get_db(self):
        return self.mongodb


mdb = Mdb()
# #### database operation for  msg event in linebot and save them into Mongodb
# msg_events coloection
class DataComponent:
    """
    # The sub-class uses __init__(self,dict_obj=None,isCopy=True):
    # if dict_obj is none, _model_fields will be copy to self.data

    use template example:

    --------------------------------
    class ClassTemplate(DataComponent):


    # model fields can be check and accessed if needed by self.model_fields but it is readonly




        _model_fields = {
            #'_id':'',     # ourse section id  -- will be auto assiged by database
            'course_series_id': 'series id',
            'title_en':'title en',
            'cs_topics': []    # seperated with CourseSection to avoid too many layers in database schema
        }


        # Use DataComponent __init__ Or override __init__:
        # if dict_obj is none, _model_fields will be copy to self.data
        # you can override __init__ like following
        def __init__(self,dict_obj=None,isCopy=True):
            try:
                # get default data from _model_fields  (self.data = _model_fields)
                super().__init__(dict_obj,isCopy)
                # do customized thing here
                self.data["test"] = "unitest is great!"

            except Exception as e:
                #from tzm.base import print_error
                print_error(e)
    """

    def __init__(self, dict_obj=None, isCopy=True):
        # construct will make deep copy by default
        if dict_obj != None:
            if type(dict_obj) is not dict and type(dict_obj) is not OrderedDict:
                raise TypeError("dict_obj should be dictionary or OrderedDict")
            if isCopy == True:
                self.data = copy.deepcopy(dict_obj)
            else:
                self.data = dict_obj
            if not self.isFieldsMatches(dict_obj):
                print("Warnning! the initial fields does not match default keys")
        else:
            self.data = copy.deepcopy(self._model_fields)

    ####################################3333333
    # data strcuture section
    _model_fields = [
        {
            "key_name1": "default_value1",
            "key_name2": "default_value2",
        }
    ]

    @property
    def model_fields(self):
        # return mongodb collection object so that the API can be used directly
        return self._model_fields

    @model_fields.setter
    def model_fields(self, value):
        raise AttributeError("col is not a writeable attribute")

    ##############################    class object operations    #######################################

    @classmethod
    def notCopy(cls, dict_obj=None):
        if dict_obj == None:
            raise TypeError("object_list cannot be None")
        if type(dict_obj) is not dict and type(dict_obj) is not OrderedDict:
            raise TypeError("dict_obj should be dictionary or OrderedDict")
        return cls(dict_obj=dict_obj, isCopy=False)

    @classmethod
    def get_object_list(cls, object_list=None, isCopy=True):
        """
        construct class objects list from object list
        """
        try:
            if type(object_list) is not list:
                raise TypeError("object_list is not list")
            if object_list == None:
                raise TypeError("object_list cannot be None")
            if object_list == []:
                raise TypeError("Warning! object_list should not be empty list")
                return []

            cls_list = []
            for item in object_list:
                if isCopy:
                    cls_item = cls(item)
                else:
                    cls_item = cls.notCopy(item)

                cls_list.append(cls_item)

            return cls_list
        except Exception as e:
            print(e)

    @classmethod
    def get_object_list_notCopy(cls, object_list=None):
        return cls.get_object_list(object_list=object_list, isCopy=False)

    def setField(self, field=None, field_obj=None):
        """
        if field_obj == None, then set the field = None
        if there is no field, then it would create a field with the fieldname=None
        """
        try:
            if field == None:
                raise TypeError("code error", "setField() -- Object is needed")
            else:
                if field_obj == None:
                    print(f"setField: Warning!!! field_obj is None. field={field}")

                if field not in self.data:
                    print(
                        f"Warning!!! the field <{field}> Not in curret field set <-- {self.data}"
                    )
                    print(f"Adding the field {field} to object")
                self.data[field] = field_obj
        except Exception as e:
            print(e)

    def getField(self, field=None):
        if field not in self.data:
            raise TypeError("Not valid field")
        return self.data[field]

    def delField(self, field=None):
        if field in self.data:
            del self.data[field]
        else:
            print(f"Warning!!! : delField()  {field} field does not exists")
            # DEBUG code
            # print "the word is ", self.data

    def addNewField(self, field=None, default_value=None):
        if field == None:
            raise TypeError("field cannot be None")
        if field in self.data:
            raise KeyError(
                f"Warning!!! addNewField() {field} field is ready in the object"
            )
            print(f"Warning!!! addNewField() {field} field is ready in the object")
        else:
            if default_value != None:
                self.data[field] = default_value
            else:
                self.data[field] = None

    def isFieldsMatches(self, fields_dict=None):
        """
        Tools for check fields keys are correct
        """
        if fields_dict == None:
            fields_dict = self.model_fields
        for key in self.data:
            if not key in fields_dict:
                return False
            return True

    def getData(self):
        return self.data

    def setData(self, dict_obj=None):  # !!! assign not copy
        if dict_obj != None:
            if type(dict_obj) is not dict and type(dict_obj) is not OrderedDict:
                raise TypeError("dict_obj should be dictionary or OrderedDict")
            self.data = dict_obj
        else:
            raise TypeError("dict_obj is required")

    def printData(self):
        print("Data Object:  ")
        p = pprint.PrettyPrinter(indent=4)
        p.pprint(self.data)

    def existsField(self, field_str):
        if type(field_str) is not str:
            raise TypeError("field_str must be string")
        return field_str in self.data

    def hasField(self, field_str):
        if type(field_str) is not str:
            raise TypeError("field_str must be string")
        return field_str in self.data

    def saveJsonToFile(self, fp):  # write data component in json
        try:
            json.dump(
                self,
                fp,
                ensure_ascii=False,
                default=data_component_json_serialized,
                indent=3,
            )

        except Exception as e:
            print_error(e)

    def loadJson(self, s):
        try:
            data_dict = json.loads(s)
            self.data = data_dict
        except Exception as e:
            print_error(e)

    def loadJsonFromFile(self, fp):
        """load data component in json
        Currently Mongodb is ObjectID is not supported."""
        try:
            data_dict = json.load(fp)
            self.data = data_dict
        except Exception as e:
            print_error(e)

    def addToListField(self, field_name, item_to_add):
        pass

        """ return False if item_to_add is already in the list  
            return True if added"""
        try:
            list_field = self.getField(field_name)
            if type(list_field) is not list:
                raise TypeError(f"The field {field_name} is not a list")
            # check it is in the list already
            if item_to_add not in list_field:
                list_field.append(item_to_add)
                return True
            else:
                raise KeyError("Warrning! item exists already.")

        except Exception as e:
            print_error(e)

    def removeFromListField(self, field_name, item_to_add):

        """return True if item_to_add is already in the list, and remove it done!
        return False if there is no item_to_add in the list"""
        try:
            list_field = self.getField(field_name)
            if type(list_field) is not list:
                raise TypeError(f"The field {field_name} is not a list")
            # check it is in the list already
            if item_to_add not in list_field:
                print("Warrning! The item is not in the list. Nothing removed")
                return False
            else:
                list_field.remove(item_to_add)
                return True

        except Exception as e:
            print_error(e)

    def searchListField(self, field_name, match_f, **kwargs):
        """
        match_f is a match function
        """
        the_list = self.data[field_name]
        if type(the_list) != type([]):
            raise TypeError("the field should be a list")
        for item in the_list:
            if match_f(item, kwargs):
                return item


class DbDataCo(DataComponent):

    """
    # The sub-class uses __init__(self,dict_obj=None,isCopy=True):
    # if dict_obj is none, _model_fields will be copy to self.data

    use template example:
    class ClassTemplate(DataComponent):

    ################### begin col ##########################################33
    # __qualname__ == class name and will NOT inherit from base class => every datacomponent child needs to have these two lines
    col_name = __qualname__
    col = mdb.get_db()[__qualname__]
    #################### end col ############################################
    # model fields can be check and accessed if needed by self.model_fields but it is readonly




        _model_fields = {
            #'_id':'',     # ourse section id  -- will be auto assiged by database
            'course_series_id': 'series id',
            'title_en':'title en',
            'cs_topics': []    # seperated with CourseSection to avoid too many layers in database schema
        }

        _db_index_list = [IndexModel([("key_name1", DESCENDING)], unique=True)]
        #For index definition,
        #refer to https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index




        # Use DataComponent __init__ Or override __init__:
        # if dict_obj is none, _model_fields will be copy to self.data
        # you can override __init__ like following
        def __init__(self,dict_obj=None,isCopy=True):
            try:
                # get default data from _model_fields  (self.data = _model_fields)
                super(ClassTemplate, self).__init__(dict_obj,isCopy)
                # do customized thing here
                self.data["test"] = "unitest is great!"

            except Exception as e:
                #from tzm.base import print_error
                print_error(e)




    ##########################################################
    Line testing:
    event_template = {
        "message":  {"id": "14339762965727", "text": "I would like to have Santiago cake. ", "type": "text"},
        "mode": "active",
        "replyToken": "90283169cf71442eaa46c0f3905a3c7b",
        "source": {"type": "user", "userId": "U8c0f51197c2eb9ec822878cbc35c451c"},
        "timestamp": 1625462823884, "type": "message"
    }
    """

    ##############################################3
    # database section
    _db = mdb

    # static class name: PEP 3155 introduced __qualname__, which was implemented in Python 3.3.
    # refer to https://stackoverflow.com/questions/6943182/get-name-of-current-class
    # need to copy to the child class as well.
    ################### begin col ##########################################33
    # __qualname__ == class name and will NOT inherit from base class => every datacomponent child needs to have these two lines
    col_name = __qualname__
    col = mdb.get_db()[__qualname__]
    #################### end col ############################################
    _db_index_list = [IndexModel([("key_name1", DESCENDING)], unique=True)]
    # For index definition,
    # refer to https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
    # from pymongo import IndexModel, ASCENDING, DESCENDING
    # index1 = IndexModel([("key1", DESCENDING),
    #                      ("key2", ASCENDING)], name="hello_world")
    # index2 = IndexModel([("goodbye", DESCENDING)])
    # db.test.create_indexes([index1, index2])

    def __init__(self, dict_obj=None, isCopy=True):
        # construct will make deep copy by default
        super().__init__(dict_obj, isCopy)

        # Create index
        type(self)._col = self.col
        self.col.create_indexes(self.db_index_list)

    @property
    def db_index_list(self):
        return self._db_index_list

    @db_index_list.setter
    def db_index_list(self, value):
        raise AttributeError("db_index_list is not a writeable attribute")

    @property
    def id(self):
        """
        login_user() need self.id as a unique key to put in session data.
        """
        if not "_id" in self.data:
            raise KeyError(f"{type(self)} does not have _id field!")
        return self.data["_id"]

    # @property
    # def db(self):
    # show NOT be used in normal data operation unless you need to change database Configuration
    #    return _db.db

    # @db.setter
    # def db(self, value):
    #    raise AttributeError("db is not a writeable attribute")

    # @property
    # def col(self):
    # return mongodb collection object so that the API can be used directly
    #    return self._db.get_db()[self.__class__.__name__]

    # @col.setter
    # def col(self, value):
    #    raise AttributeError("col is not a writeable attribute")

    def insert_doc_with_extra(self, doc, extra_info=None):
        # def insert_doc(self, doc, extra_info=None):
        if extra_info != None:
            doc["Extra_info"] = extra_info
        return self.col.insert_one(doc)

    def insert_doc(self, extra_info=None):
        # def insert_doc(self, doc, extra_info=None):
        if extra_info != None:
            doc["Extra_info"] = extra_info
        return self.col.insert_one(self.data)

    def delete_doc(self, query):
        return self.col.delete_one(query)


if __name__ == "__main__":
    try:
        # load db from json file, default: db_info.json
        mdb_for_test = Mdb(db_info_file="db_info.json")

        print("show databases: ")
        print(mdb_for_test.get_db().client.list_database_names())
        print("mdb get_db =")
        tzdb = mdb_for_test.get_db()
        print(tzdb)

        data1 = {
            "key_name1": "joseph",
            "key_name2": 256,
        }
        data2 = {
            "key_name1": "joe",
            "key_name2": 256,
        }
        data3 = {
            "key_name1": "jos4eph",
            "key_name2": 256,
        }
        dr1 = DbDataCo(data1, isCopy=False)
        dr2 = DbDataCo(data2, isCopy=False)
        dr3 = DbDataCo(data3, isCopy=False)
        print("Great!")
        try:
            dr1.col.insert_one(dr1.data)
            dr2.col.insert_one(dr2.data)
            dr3.col.insert_one(dr3.data)
        except Exception as e:
            print_error(e)

        linebot_msgevent = {
            "message": {
                "id": "14339762965727",
                "text": "I would like to have Santiago cake. ",
                "type": "text",
            },
            "source": {"type": "user2", "userId": "U8c0f51197c2eb9ec822878cbc35c451c"},
            "timestamp": 1625462823884,
            "type": "message",
        }
        # print("before insert")
        # msgs.insert_doc_with_extra(linebot_msgevent)

        # print("before find")
        # pprint.pprint(msgs_dbcol.find_one())
        # msg_events = msgs.find_event_with_userid("U8c0f51197c2eb9ec822878cbc35c451c")
        # for msg_event in msg_events:
        #    pprint.pprint(msg_event)

        # result = msgs.delete_doc(
        #    {
        #        "source.userId": "U8c0f51197c2eb9ec822878cbc35c451c",
        #    }
        # )
        # if result == None:
        #    print("result is None")
        # else:
        #    pprint.pprint(result)
        #    print(f"result.deleted_count:  {result.deleted_count}")

    except Exception as e:
        print_error(e)

else:
    # open database configruation by default value
    pass
    # mdb = Mdb()

    # collection linebot msg events
