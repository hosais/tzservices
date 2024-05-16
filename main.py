# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com


import os
import sys
from tzm import tzservices
from tzm.item import Menu
from tzm.item import unit_test_item
from tzm.base import print_error

sys.path.insert(0, os.path.dirname(__file__))
from tzm.unit_item import price_function_unit_test

if __name__ == "__main__":
    tzservices.run()
    # test item.py
    # unit_test_item()
    #price_function_unit_test()
