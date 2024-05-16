# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
from pymongo.collection import Collection
import json
import pprint
import collections
from copy import deepcopy
from bson import ObjectId

import types
import inspect


# from tzdb import mdb

# print(user_cl.col.find_one({"username": "joseph"}))
#################3
# printer test
from win32printing import Printer
import win32print

"""
printer = Printer(linegap=1, printer_name="CP-Q3")
printer.text("text 測試")



p = win32print.OpenPrinter ("Adobe PDF")
job = win32print.StartDocPrinter (p, 1, ("test of raw data", None, "RAW")) 
win32print.StartPagePrinter(p) 
win32print.WritePrinter(p, b"ddfgsdfgsdfgsfdgsdfffffffffgddfddfgdfgfdgata to print") 
win32print.WritePrinter(p, b"ddfgsdfgsdfgsfdgsdfffffffffgddfddfgdfgfdgata to print") 
win32print.WritePrinter(p, b"ddfgsdfgsdfgsfdgsdfffffffffgddfddfgdfgfdgata to print") 
win32print.WritePrinter(p, b"ddfgsdfgsdfgsfdgsdfffffffffgddfddfgdfgfdgata to print") 
win32print.WritePrinter(p, b"ddfgsdfgsdfgsfdgsdfffffffffgddfddfgdfgfdgata to print") 
win32print.EndPagePrinter (p)


from glob import glob

# A List containing the system printers
all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
# Ask the user to select a printer
printer_num = int(input("Choose a printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n"))
# set the default printer
win32print.SetDefaultPrinter(all_printers[printer_num])
pdf_dir = "E:\hosai\test.pdf"
for f in glob(pdf_dir, recursive=True):
    win32api.ShellExecute(0, "print", f, None,  ".",  0)

input("press any key to exit")



#######################

"""


class ttt:
    pass


class Test(ttt):
    #   _db = mdb
    tt = __qualname__
    #   _col = _db.get_db()[_col_name]
    db_name = "tzdb"
    db_user = "tzmongo"
    db_host_DN = "tzcluster.fp5yu.mongodb.net"
    db_pw = "pymonjoe1"

    def __init__(self, isCopy=False, **kwarg) -> None:

        print(isCopy)
        for key, value in kwarg.items():
            value2 = deepcopy(value)
            setattr(self, key, value2)
        print("end")

    # def __init__(self, dict) -> None:
    #   for key, value in dict.items():
    #      setattr(self, key, value)
    def print_class_name(self):
        print(self._col_name)

    @property
    def col_name(self):
        return self.__class__.__name__

    @property
    def password(self):
        return self.password

    def dict_getattr_test(self):
        fp = open("db_info.json")
        jod = json.load(fp, object_pairs_hook=collections.OrderedDict)
        for key, value in jod.items():
            # print(f"key={key}")
            setattr(self, key, value)
        # self = self.__class__( json.load(fp, object_hook=lambda d: SimpleNamespace(**d)))
        # self = Test()
        print("*********************in dict_get_attr_Test()")
        print(jod)
        # print(self)
        print("ordered_preserved")
        print(list(Test.__dict__.keys()))
        fp.close()
        self.db_name = "test"
        print(f" change db_name to {self.db_name}")
        print("************dict_get_attr_Test() finished")

    def set_db_name(self):
        self.db_name = "oh mine!"

    def print_all_values(self):
        for key, value in __dict__:
            print(f"self.{key} is {value}")

    @classmethod
    def print_class_db_name(cls):
        print(f"class.db_name is {cls.db_name}")

    def printDataObj(self):
        print("Data Object:  ")
        p = pprint.PrettyPrinter(indent=4)
        p.pprint(self)


t3 = Test()
t4 = Test(fun="test", isCopy=True)
t5 = Test(fun="testfun")
# pprint.pprint(vars(t3))

print(f"t3 == the object print with dict = {vars(t3)}")

t4.set_db_name()

# t4.dict_getattr_test()
print(f"t4 == the object print with dict = {vars(t4)}")


print(f"t5 == the object print with dict = {vars(t5)}")
print("t5 class db name")
t5.print_class_db_name()
print("t4 class db name")
t4.print_class_db_name()
print("t3 class db name")
t3.print_class_db_name()
print(f"t5 self.db_name = {t5.db_name}")

# using __dict__ to access attributes
# of the object n along with their values
print(t5.__dict__)

# to only access attributes
print(t5.__dict__.keys())

# to only access values
print(t5.__dict__.values())
print("####################33")
print(f"t4 = {dir(t4)}")

print(f" t5 col name = {t5.col_name}")
print(f" t4 col name = {t4.col_name}")
print(f"class db_name ={Test.db_name}")
print(Test.tt)

# print(t2.joseph)
# print(t2.python)
