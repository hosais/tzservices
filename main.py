# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com


import os
import sys
from tzm import tzservices

sys.path.insert(0, os.path.dirname(__file__))


if __name__ == "__main__":
    tzservices.run()
