# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
# product.py is mainly for calculating the product price for POS device in Taro Zafra
# This file 
#
#

''' ***********   Rule functions ***********
       Rule function can be few types: 
           1) special group ingredient (3Q, taro balls  ...)
           2) max_type (less than ...)
           3) more to be updated
    ****************************************
'''
import re



class price_rule():    
    '''
        # rule list ex: rules = [max75_r, if_taro_combo_r]
        
        # must to be the function with the form of 
        #   def RuleFunctionInterface(product_str="TestingRule_product_str", ori_price=100, para1="NULL", para2="NULL2"):
        #   para1, para2 are extra parameters
    '''
    index_of_key = 2
    index_of_para=1
    index_of_func_name=0

    rule_rank = lambda rule : rule[price_rule.index_of_key]  # used by list order fucntion for get the key so that the rule would be applied first
    # a rule function should be a class statis method with parameter (product_str, ori_price, parameters ...) 
    
    # class function without class parameter
    @staticmethod
    def RuleFunctionInterface(product_str="TestingRule_product_str", ori_price=100, para1="NULL", para2="NULL2"):
        '''
        Rule function prototype
        at least need to hvae product_str and ori_price parameters
        '''
        print("RuleFunction_Interface is called")        
        print(f"product_str = {product_str}")
        print(f"ori_price = {ori_price}")
        print(f"para1={para1}")   
        print(f"para2={para2}")  
        error_message = None
        updated_price = ori_price    
        return error_message, updated_price
    @staticmethod
    def max_price(product_str, ori_price, max_price = 0):
        '''
            if the price is bigger than max_price, the max price returned
        '''
        error_message = None
        updated_price = max(ori_price,max_price)
        return None, updated_price
        
       

    @staticmethod
    def if_taro_combo(product_str, ori_price):
        '''
            checked replace the group ingredient name, such as 3Q

        '''
        # get the set of ingredients
        # 
        # take parts with the symbol '+'
        extra_symbol = "\\+"  # extra  for regex string requirement
        parts = re.split(
            extra_symbol, product_str
        )  # parts should be "ingredient" or "ingredient x #" forms.

        error_message = None
        updated_price = ori_price
        threeQ = {"芋圓", "地瓜圓", "黑糖粉粿"} 
        #print(product_str + "should check there are taro_combo or not")
        print(f"of_taro_combo: product_str = {product_str}, ori_price = {ori_price}")
        return error_message, updated_price









        
    def rule_body_f(self, func_name,  **kwargs):  
        ''' call rule functions in rule_price class
            access the function variable by getattr of the class
            to call a method:   <function variable>+()
            use the function_name_string to retrive the function variable and then call it with () operator
            '''
        
        print(f"************func_name:{func_name}")  
        print(f"parameters = {kwargs}") 
        
          
        # get fucntion variable
        func = getattr(price_rule,func_name)        
        print(f"apply the func {func_name} with parameters {kwargs}")
        error_message , price= func(**kwargs)
        print(f"error message = {error_message}, return price = {price}")
        return error_message, price
        


    def apply_all_rule_f(self,product_str,ori_price,rules):
        '''
        Apply rules functions
            The rule function should be 
              =>  rule_f(self, func_name, **kwargs)
                    return error_message, price
                    return error_message == None <= no_error
        

        '''
        # MAKE SURE THE RULE FUNCTION IS IN ORDER 
        rules.sort(key=price_rule.rule_rank)
        updated_price=ori_price
        print (f"apply_rule_f: rules = {rules}")
        for rule in rules:
            # function name: print(f"apply_rule_f: rule[0] = { rule[0]}")         
            # parameters: print(f"apply_rule_f: rule[1] = { rule[1]}")
            # add parameters for every rule
            kwargs = rule[1]
            kwargs["ori_price"] = ori_price
            kwargs["product_str"] = product_str
            #print(f"apply_rule_f: will apply rules with parametes = { kwargs}")
            error_message, updated_price = self.rule_body_f(rule[0],**kwargs)
            if error_message != None:
                return error_message, 0
            ori_price=updated_price
            
            
        return error_message, updated_price    



    def unit_test_price_rule():
        #rules sample
        
        dummy_rule = ("RuleFunctionInterface",{"para1":"p1_value", "para2": "p2_value"},10) # priority 10 (normal)
        max75_r = ("max_price",{"max_price": 75},12)
        if_taro_combo_r = ("if_taro_combo", {},9)  # None parameter would be a empty dictionary, so that it can still add product_str and price in the dictionary
        pr = price_rule()
        rules = [dummy_rule, max75_r,if_taro_combo_r]
        ordered_rules = [if_taro_combo_r, dummy_rule, max75_r]
        temp_rules = rules.copy()
        if temp_rules == ordered_rules:
            print("rules have been ordered, test may be not effective")    
        temp_rules.sort(key=price_rule.rule_rank)
        if temp_rules == ordered_rules:
            print("rule order test passed")
        else:
            print("rule order pass failed")
        
            
        error_message, price = pr.apply_all_rule_f("豆花",45,rules)
        
        
        if price != 45 or error_message != None:
            print(f"Failed: price shoud be 45!, price = {price}")
            print(f"error_message = {error_message}")
        else:
            print("test passed")
    
    



'''=====================END Rule functions =========================================================


=====================END Rule functions =========================================================
'''

##############################################################################
#    Copyright (C) 2015 - Present, Braincrew Apps (<http://www.braincrewapps.com>). All Rights Reserved

# Odoo Proprietary License v1.0
#
# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps,  braincrewapps.com, or if you have received a written
# agreement from the authors of the Software.
#
# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

##############################################################################

import re
import os

os.system("")
from odoo import api, fields, models, _


base_items = [
    {"name": "冰", "e_name": "Ice", "price": 0, "extra_price": 0, "default_ingredient_extra_price": 10},
    {"name": "優格", "e_name": "Yogurt", "price": 50, "extra_price": 7, "default_ingredient_extra_price":5},
    {"name": "披薩", "e_name": "Pizza", "price": 100, "extra_price": 8, "default_ingredient_extra_price":5},
]
ingr_items = [
    {"name": "花生", "e_name": "Peanut", "price": 30},
    {"name": "芒果", "e_name": "Mango", "price": 30, "extra_price": 15},
    {"name": "巧克力", "e_name": "Chocolate", "price": 30},
]


DEFAULT_EXTRA_PRICE = 5

class ProductProduct(models.Model):
    _inherit = 'product.product'

  


    def match_name(self,pass_item, in_items_info):
        for item in in_items_info:
            print(pass_item,'++++++++++++++++++++++++++++++----------------------match name------', in_items_info)
            if pass_item == item["name"] or pass_item == item["e_name"]:
                print('+++++++++++++++++++-match_name---------------------itemitemitemitem--------------',item)
                return item
        return None

    def match_all_item(self,extra_ingredient):
        print(">>>>>>>>>>extra_ingredient",extra_ingredient)
        # print(">>>>>>>>>>base_items",base_items)/
        # print(">>>>>>>>>>ingr_items",ingr_items)
        """return None if no item found"""
        print(">>>>>>>extra_ingredient",extra_ingredient, base_items)
        matched_ingr = self.match_name(extra_ingredient, base_items)
        print(">>>>>>fff>>>>matched_ingr",matched_ingr)
        if matched_ingr == None:
            # search ingr
            matched_ingr = self.match_name(extra_ingredient, ingr_items)
        return matched_ingr

    def extra_price_inte(self,product_str, extra_ingredient, odoo_standard=False):
        """
        It returns extra price, error_message. If no error => price, None. If there is something wrong, price=0(undefined), error_message = "error message".

        product_str: the DCP name (sepreated by space and "+" )
        extra_ingredient: the name of extra ingredient
        odoo_standard == True. the product_str is NOT a DCP( Dynamic combination product)
        odoo_standard == False. the product_str is a DCP
        1) This function returns extra price of an ingredient, so that the UI can show the extra price
        2) For some special products, there are special extra prices.
        3) odoo_standard = True => odoo standard product with extra ingredient. In this case, default value would be used unless there is a extra price of on ingredient itself.
           If odoo_stardard==False, if there is NO extra ingredient price specified => return 5. Or return 10 if there is "ice" in the name.
        4) The extra price function return to UI, is for showing the user information in UI. The calculation is still in total_price_inte()
        5) When base is used, extra price field would be used as extra price. (just like ingredient that has extra price. Note: all bases have extra price field)
        """

        print('-----------extra_price_inte-------product_str--------11----',product_str)
        print('-----------extra_price_inte-------extra_ingredient---12-----',extra_ingredient)
        print('-----------extra_price_inte-------odoo_standard---13-----',odoo_standard)
        # DEFAULT_EXTRA_PRICE = 5
        # ICE_EXTRA_PRICE = 10
        matched_ingr = self.match_all_item(extra_ingredient)
        print('--------extra_price_inte----------15------------',matched_ingr)
        if matched_ingr == None:
            # error_message_new = product_str + ' ' + extra_ingredient
            # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',error_message_new)
            error_message = "NOT defined ingredient"
            print('--------------------------extra_price_inte------------------------------------extra_price_inte-----------------------------',error_message)
            print('-----extra_price_inte--------16-------',error_message)
            return 0, error_message
            # Currently not defined return 0

        if "extra_price" in matched_ingr: # if there is extra ingredient price( have extra_price)
            print('++++++++++999999999999---------------matched_ingr---------------------',matched_ingr["extra_price"])
            return matched_ingr["extra_price"], None
        else:  # NO extra price =>default value
            if odoo_standard:
                return DEFAULT_EXTRA_PRICE, None
            else:  # It is DCP (NOT odoo standard product)
                ########################### take out extra part, with '+' symbol
                if product_str == "":
                    error_message = str(product_str) + str(extra_ingredient) + str(product_str)
                    error_message = error_message + '\r\n' + "Nothing selected"
                    print('--------extra_price_inte----------17-----',error_message)
                    return 0, error_message
                if type(product_str) != str:
                    error_message = str(product_str) + ',' + str(extra_ingredient) + str(odoo_standard)
                    error_message = error_message + '\r\n' + "Prodcut_str is not a string"
                    print('----------extra_price_inte---------18----------',error_message)
                    return 0, error_message

                # take parts with the symbol '+'
                extra_symbol = "\+"  # extra  for regex string requirement
                parts = re.split(
                    extra_symbol, product_str
                )  # parts should be "ingredient" or "ingredient x #" forms.
                print('-------extra_price_inte-------19--------parts------',parts)
                ############ preparing dynamic production combination
                dpc = 0  # dynamic product combination
                # Note: string split() also remove space characters
                dpc_str_temp = parts.pop(dpc)
                dpc_str = dpc_str_temp.strip()  #  <<---- to see there are easier way?
                ingr_in_product = dpc_str.split()

                base_str = ingr_in_product[-1]
                base_pair = self.match_all_item(base_str)
                print('-------extra_price_inte-----------base_pair-------20-----',base_pair)
                if base_pair != None:
                    if "default_ingredient_extra_price" in base_pair:
                        print('----------extra_price_inte-----------base_pair-------21------------',base_pair["default_ingredient_extra_price"])
                        return base_pair["default_ingredient_extra_price"],None
                    else:
                        print('-------------extra_price_inte-----------base_pair-------22--------------')
                        return 0, "No default extra price in base data"
                else:
                    print('----------extra_price_inte-----------base_pair--------23--------')
                    return 0, "no base found in product string,  base = " + base_str

                #################################
                # if "冰" in ingr_in_product or "Ice" in ingr_in_product:
                #     print('+----------extra_price_inte-----------base_pair--------24------------',ICE_EXTRA_PRICE)
                #     return ICE_EXTRA_PRICE, None
                # else:
                #     print('--------extra_price_inte-----------base_pair--------25---------',DEFAULT_EXTRA_PRICE)
                #     return DEFAULT_EXTRA_PRICE, None


    def total_price_inte(self,product_str):
        """
        only for integration test
        The total price: the price can be calculated by a product name string form such as
                  <ingredient1> <ingredient2> … <base> + <extra1>x2 + <extra2>.
        a python function ourselves:
                  total_price, error_message = func(product_str).

        It return prices, error_message. If no error => price, None. If there is something wrong, price=0(undefined), error_message = "error message".



        the NP names are in Chinese only.
        For testing purpose, the NP_name_samples includes english string too.
        NP_name_samples: Normalized NP Name

        ###Base
        冰 Ice  0
        優格  Yogurt 50
        披薩  Pizza 100
        ### Ingredients
        花生 Peanut   <-- No base (error)          order# 1
        芒果 Mango   <-- No base (error)           order# 2
        巧克力 Chocolate <-- No base (error)       order# 3



        ### Dynamic combinations
        花生 芒果 披薩 Peanut Mango Pizza 250
        巧克力 優格 Chocolate Yogurt 130
        花生 芒果 巧克力 優格 Peanut Mango Chocolate Yogurt 230
        花生 冰  Peanut Ice 60


        Errors:
        花生 芒果 巧克力  Peanut Mango Chocolate <-- no base
        巧克力 披薩 Chocolate Pizza <--  Cannot add this ingredient to pizza


        NOT defined <--- Undefined or NOT acceptable combinations
        """

        ##################### Init
        print('55555555555555---------------------------------------------------',product_str)
        total_price = 0
        error_message = None

        dynamic_combinations = [
            {"name": "冰", "e_name": "Ice", "price": 0},
            {"name": "優格", "e_name": "Yogurt", "price": 50},
            {"name": "披薩", "e_name": "Pizza", "price": 100},
            {"name": "花生 芒果 披薩", "e_name": "Peanut Mango Pizza", "price": 250},
            {"name": "巧克力 優格", "e_name": "Chocolate Yogurt", "price": 130},
            {
                "name": "花生 芒果 巧克力 優格",
                "e_name": "Peanut Mango Chocolate Yogurt",
                "price": 230,
            },
            {"name": "花生 冰", "e_name": "Peanut Ice", "price": 60},
        ]
        wrong_dynamic_combinations = [
            {
                "name": "花生 芒果 巧克力",
                "e_name": "Peanut Mango Chocolate",
                "error_message": "no base",
            },
            {
                "name": "巧克力 披薩",
                "e_name": "Chocolate Pizza",
                "error_message": "Error: Cannot add this ingredient to pizza",
            },
        ]
        ########################### take out extra part, with '+' symbol
        if product_str == "":
            return 0, "Nothing selected"
        if type(product_str) != str:
            return 0, "Prodcut_str is not a string"
        # take parts with the symbol '+'
        extra_symbol = "\+"  # extra  for regex string requirement
        parts = re.split(
            extra_symbol, product_str
        )  # parts should be "ingredient" or "ingredient x #" forms.
        print('--------total_price_inte------part---31------',parts)
        ############ preparing dynamic production combination
        dpc = 0  # dynamic product combination
        # Note: string split() also remove space characters
        dpc_str_temp = parts.pop(dpc)
        dpc_str = dpc_str_temp.strip()  #  <<---- to see there are easier way?
        ingr_in_product = dpc_str.split()

        #print(f"dynamic product combination string: {dpc_str}")
        ############## preparing extra ingredients
        no_space_parts = [x.replace(" ", "") for x in parts]

        #print(f"extra = {no_space_parts}")

        ############################# Must to have base
        has_base = False
        print('--------total_price_inte---------ingr_in_product-------32----',ingr_in_product)
        for item in ingr_in_product:
            base_str = item
            if self.match_name(item, base_items) != None:  # matched
                has_base = True
                break

        if not has_base:
            error_message =  str(product_str)
            error_message = error_message + ' ' +"Error: No base"
            print('------total_price_inte------ingr_in_product-------33----',ingr_in_product)
            return 0, error_message


        # Matched? return price
        matched_product_info = self.match_name(dpc_str, dynamic_combinations)

        #print(f"matched_product_info= {matched_product_info}")
        if matched_product_info != None:
            total_price = matched_product_info["price"]
            error_message = None

        else:
            # check what kind of error
            matched_product_info = self.match_name(dpc_str, wrong_dynamic_combinations)
            print('------------total_price_inte--------matched_product_info--------34-----',matched_product_info)
            if matched_product_info != None:
                return 0, matched_product_info["error_message"]
            else:
                # Undefined? return error message
                return 0, "Error: Undefined or NOT acceptable combinations"

        ####### add extra parts to total price
        print('----------total_price_inte----------no_space_parts0-------35------',no_space_parts)
        for extra_str in no_space_parts:
            print('----------total_price_inte----------no_space_parts0-------215-----')
            #print(f"txtra_str = {extra_str}")
            extra_list = extra_str.split("*")
            extra_ingredient = extra_list[0]
            if len(extra_list) == 2:
                extra_quantity = int(extra_list[1], base=10)
            else:
                extra_quantity = 1  # no "x #" = > default value =1
            # print(f"extra = {extra_ingredient}")
            # print(f"extra quantity = {extra_quantity}")
            matched_ingr = self.match_all_item(extra_ingredient)
            print('>>>320>>matched_ingr>', matched_ingr)
            # final result
            if matched_ingr != None:
                print(base_str,'####condi matched_ingr#######323', matched_ingr)
                # check some error combination here
                
                if base_str == "冰" or base_str == "Ice":
                    print('####base_str#######326', base_str)
                    if extra_ingredient == "Pizza" or extra_ingredient == "披薩":
                        return 0, "Error: Ice cannot add pizza"
                # get extra price and add it in total
                print('#########328###############', product_str,'>>>>>>>>>>>>>>>>>', extra_ingredient)
                # print('#########329###############', ep, ep_error_message)
                ep, ep_error_message = self.extra_price_inte(
                    product_str, extra_ingredient, odoo_standard=False
                )
                print('-------------total_price_inte-----------ep_error_message---------36---------',ep_error_message)
                print('---------------total_price_inte------------ep_error_message--------37--*----',ep)
                print(">>>>>>>>>ep_error_message",ep_error_message)
                if ep_error_message == None:
                    # print(f"extra_ingredient = {extra_ingredient}, ep = {ep}")
                    total_price += ep * extra_quantity
                else:
                    return 0, ep_error_message
            else:
                return 0, "Error: Extra undefined Extra or NOT acceptable combinations"

        # correct return
        print('---------total_price_inte----------------total_price--------------38-------------',total_price)
        print('---------total_price_inte----------------error_message--------------39-------------',error_message)
        return total_price, error_message
        #################33 unit test


    def price_function_unit_test(self):
        menu_item_names = [
            ("冰", "Ice", 0),
            ("優格", "Yogurt", 50),
            ("披薩", "Pizza", 100),
            ("花生", "Peanut", "Error: No base"),
            ("芒果", "Mango", "Error: No base"),
            ("巧克力", "Chocolate", "Error: No base"),
            ("花生 芒果 披薩", "Peanut Mango Pizza", 250),
            ("巧克力 優格", "Chocolate Yogurt", 130),
            ("花生 芒果 巧克力 優格", "Peanut Mango Chocolate Yogurt", 230),
            ("花生 冰", "Peanut Ice", 60),
            ("花生 芒果 巧克力", "Peanut Mango Chocolate", "Error: No base"),
            ("巧克力 披薩", "Chocolate Pizza", "Error: Cannot add this ingredient to pizza"),
            ("我不喜歡", "slkdjflsk", "Error: No base"),
            ("我不喜歡 披薩", "IDoLike Pizza", "Error: Undefined or NOT acceptable combinations"),
            (
                "花生 芒果 披薩 + 巧克力",
                "Peanut Mango Pizza + Chocolate",
                250 + 5,
            ),  # extra without special price (take base default extra price)
            (
                "花生 冰 + 巧克力*2 + 芒果*3",
                "Peanut Mango Pizza + Chocolate",
                60 + 10 * 2 + 15 * 3,
            ),  # ice special extra price = 10, Mango has its own extra price
            (
                "花生 冰 + 巧克力*1 + 芒果*3+優格*1",  # Yogour is base so take its own extra price ???
                "Peanut Ice + Chocolate*1 + Mango*3 + Yogurt*1",
                60 + 10 * 1 + 15 * 3 + 7 * 1,
            ),
            (
                "花生 冰 + 巧克力*1 + 芒果*3+披薩*1",
                "Peanut Ice + Chocolate*1 + Mango*3 Pizza*1",
                "Error: Ice cannot add pizza",
            ),
            (
                "花生 芒果 披薩 + 冰", 
                "Peanut Mango Pizza + Ice" ,
                250+0,
            ),
            ("", "", "Nothing selected"),
        ]

        print('--------price_function_unit_test---------menu_item_names--------51--------',menu_item_names)
        for name, e_name, msg_or_price in menu_item_names:
            total_price, error_message = self.total_price_inte(name)
            CRED = "\033[91m"
            CEND = "\033[0m"

            if error_message == None:
                if total_price != msg_or_price:
                    print("price is wrong")
                    print(f"product_name={name}")
                    print(f"price = {total_price}")
                    print(f"error_message={error_message}")
                    print(f"{CRED} !!!!!!test failed, price:  {total_price}{CEND}")
                    print(f"{CRED} !!!!!!test failed: should be  { msg_or_price} {CEND}")
                else:
                    # correct result
                    print(f"correct result  --->  {name} price is {total_price}")

            else:
                if error_message != msg_or_price:
                    print("Error message is not as expected")
                    print(f"product_name={name}")
                    print(f"price = {total_price}")
                    print(f"error_message={error_message}")
                    print(
                        f"{CRED} + !!!!!!test failed, error_message : { error_message} {CEND}"
                    )
                    print(f"{CRED}  !!!!!!test failed: should be { msg_or_price} {CEND}")

        print('--------------price_function_unit_test-------53--------------',self.name)
        return self.name

        extra_price_items = [     # product_str, extra_ingredient, extra_ingredient_english, correct extra price/error message, 
            ("花生 芒果 披薩","冰", "Ice", 0),
            ("花生 芒果 披薩","優格", "Yogurt", 7),
            ("花生 芒果 披薩","披薩", "Pizza", 8),
            ("花生 芒果 披薩","花生", "Peanut", 5),
            ("花生 芒果 披薩","芒果", "Mango", 15),
            ("花生 芒果 披薩","巧克力","Chocolate", 5),
            
            ###############
            ("花生 冰", "冰", "Ice", 0),
            ("花生 冰","優格", "Yogurt", 7),
            ("花生 冰","披薩", "Pizza", 8),
            ("花生 冰","花生", "Peanut", 10),
            ("花生 冰","芒果", "Mango", 15),
            ("花生 冰","巧克力", "Chocolate", 10),
            #############
            
            ("花生 芒果 巧克力 優格", "冰", "Ice", 0),
            ("花生 芒果 巧克力 優格","優格", "Yogurt", 7),
            ("花生 芒果 巧克力 優格","披薩", "Pizza", 8),
            ("花生 芒果 巧克力 優格","花生", "Peanut",5),
            ("花生 芒果 巧克力 優格","芒果", "Mango", 15),
            ("花生 芒果 巧克力 優格","巧克力", "Chocolate", 5),
            ########### odoo standard product
            ("odoo standard product", "冰", "Ice", 0),
            ("odoo standard product","優格", "Yogurt", 7),
            ("odoo standard product","披薩", "Pizza", 8),
            ("odoo standard product","花生", "Peanut",5),
            ("odoo standard product","芒果", "Mango", 15),
            ("odoo standard product","巧克力", "Chocolate", 5),
            
        ]
        print('--------------price_function_unit_test------------extra_price_items-------54---',extra_price_items)
        for product_str, extra_ingr, extra_ingr_en, extra_price in extra_price_items:
            if product_str == "odoo standard product":
                ep, error_message = self.extra_price_inte(product_str, extra_ingr,odoo_standard=True)
            else:    
                ep, error_message = self.extra_price_inte(product_str, extra_ingr)

            CRED = "\033[91m"
            CEND = "\033[0m"


            if error_message == None:
                if ep != extra_price:
                    print("price is wrong")
                    print(f"product_name={product_str}")
                    print(f"price = {ep}")
                    print(f"error_message={error_message}")
                    print(f"{CRED} !!!!!!test failed, price:  {ep}{CEND}")
                    print(f"{CRED} !!!!!!test failed: should be  { extra_price} {CEND}")
                else:
                    # correct result
                    print(f"correct result  --->  DCP {name}, extra {extra_ingr} extra price is {ep}")

            else:
                print(f"error message: {error_message}")


if __name__ == "__main__":
    try:
        self.price_function_unit_test()
        unit_test_price_rule()
    except Exception as e:
        self.print_error(e)
else:
    pass

  
