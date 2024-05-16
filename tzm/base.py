# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
import sys
from sys import exc_info
import traceback


FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
LineInFunc = lambda: "--> on line {}".format(sys.exc_info()[-1].tb_lineno)


def print_error(e):
    print(traceback.format_exc())
    print(e)
