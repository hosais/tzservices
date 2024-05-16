# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
'''
unit test for item class. The item is the item in the menu.


'''
import re
import os

os.system("")

base_items = [
    {
        "name": "冰",
        "e_name": "Ice",
        "price": 0,
        "extra_price": 0,
        "default_ingredient_extra_price": 10,
    },
    {
        "name": "優格",
        "e_name": "Yogurt",
        "price": 50,
        "extra_price": 7,
        "default_ingredient_extra_price": 5,
    },
    {
        "name": "披薩",
        "e_name": "Pizza",
        "price": 100,
        "extra_price": 8,
        "default_ingredient_extra_price": 5,
    },
]
ingr_items = [
    {"name": "花生", "e_name": "Peanut", "price": 30},
    {"name": "芒果", "e_name": "Mango", "price": 30, "extra_price": 15},
    {"name": "巧克力", "e_name": "Chocolate", "price": 30},
]


def match_name(pass_item, in_items_info):
    for item in in_items_info:
        if pass_item == item["name"] or pass_item == item["e_name"]:
            return item
    return None


def match_all_item(extra_ingredient):
    """return None if no item found"""
    matched_ingr = match_name(extra_ingredient, base_items)
    if matched_ingr == None:
        # search ingr
        matched_ingr = match_name(extra_ingredient, ingr_items)
    return matched_ingr


DEFAULT_EXTRA_PRICE = 5


def extra_price_inte(product_str, extra_ingredient, odoo_standard=False):
    """
    It returns extra price, error_message. If no error => price, None. If there is something wrong, price=0(undefined), error_message = "error message".

    product_str: the DCP name (sepreated by space and "+" )
    extra_ingredient: the name of extra ingredient
    odoo_standard == True. the product_str is NOT a DCP( Dynamic combination product)
    odoo_standard == False. the product_str is a DCP
    1) This function returns extra price of an ingredient, so that the UI can show the extra price
    2) For some special products, there are special extra prices.
    3) When there is no extra price specified for the ingredient, the base default extra price would be taken
    3) odoo_standard = True => odoo standard product with extra ingredient. In this case, default value would be used unless there is a extra price of on ingredient itself.
       If odoo_stardard==False, if there is NO extra ingredient price specified => return 5. Or return 10 if there is "ice" in the name.
    4) The calculation is still in total_price_inte()
    5) When ingredient is a base, the extra price is the extra_price specified in base itself, NOT default_ingredient_extra_price
    """
    matched_ingr = match_all_item(extra_ingredient)
    if matched_ingr == None:
        error_message = "NOT defined ingredient"
        print(error_message)
        return 0, error_message
        # Currently not defined return 0

    if (
        "extra_price" in matched_ingr
    ):  # if there is extra ingredient price( have extra_price)
        return matched_ingr["extra_price"], None
    else:  # NO extra price =>default value
        if odoo_standard:
            return DEFAULT_EXTRA_PRICE, None
        else:  # It is DCP (NOT odoo standard product)
            ########################### take out extra part, with '+' symbol
            if product_str == "":
                error_message = "Nothing selected"
                print(error_message)
                return 0, error_message
            if type(product_str) != str:
                error_message = "Prodcut_str is not a string"
                print(error_message)
                return 0, error_message

            # take parts with the symbol '+'
            extra_symbol = "\+"  # extra  for regex string requirement
            parts = re.split(
                extra_symbol, product_str
            )  # parts should be "ingredient" or "ingredient x #" forms.

            ############ preparing dynamic production combination
            dpc = 0  # dynamic product combination
            # Note: string split() also remove space characters
            dpc_str_temp = parts.pop(dpc)
            dpc_str = dpc_str_temp.strip()  #  <<---- to see there are easier way?
            ingr_in_product = dpc_str.split()

            #################################
            # find base
            # print(f"ingr_in_product[-1] = {ingr_in_product[-1]}")
            base_str = ingr_in_product[-1]
            base_pair = match_all_item(base_str)
            if base_pair != None:
                if "default_ingredient_extra_price" in base_pair:
                    return base_pair["default_ingredient_extra_price"], None
                else:
                    return 0, "No default extra price in base data"
            else:
                return 0, "no base found in product string,  base = " + base_str


def total_price_inte(product_str):
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

    ############ preparing dynamic production combination
    dpc = 0  # dynamic product combination
    # Note: string split() also remove space characters
    dpc_str_temp = parts.pop(dpc)
    dpc_str = dpc_str_temp.strip()  #  <<---- to see there are easier way?
    ingr_in_product = dpc_str.split()

    # print(f"dynamic product combination string: {dpc_str}")
    ############## preparing extra ingredients
    no_space_parts = [x.replace(" ", "") for x in parts]

    # print(f"extra = {no_space_parts}")

    ############################# Must to have base
    has_base = False
    for item in ingr_in_product:
        base_str = item
        if match_name(item, base_items) != None:  # matched
            has_base = True
            break

    if not has_base:
        error_message = "Error: No base"
        return 0, error_message

    # Matched? return price
    matched_product_info = match_name(dpc_str, dynamic_combinations)

    # print(f"matched_product_info= {matched_product_info}")
    if matched_product_info != None:
        total_price = matched_product_info["price"]
        error_message = None

    else:
        # check what kind of error
        matched_product_info = match_name(dpc_str, wrong_dynamic_combinations)

        if matched_product_info != None:
            return 0, matched_product_info["error_message"]
        else:
            # Undefined? return error message
            return 0, "Error: Undefined or NOT acceptable combinations"

    ####### add extra parts to total price

    for extra_str in no_space_parts:
        # print(f"txtra_str = {extra_str}")
        extra_list = extra_str.split("*")
        extra_ingredient = extra_list[0]
        if len(extra_list) == 2:
            extra_quantity = int(extra_list[1], base=10)
        else:
            extra_quantity = 1  # no "x #" = > default value =1
        # print(f"extra = {extra_ingredient}")
        # print(f"extra quantity = {extra_quantity}")
        matched_ingr = match_all_item(extra_ingredient)

        # final result
        if matched_ingr != None:
            # check some error combination here
            if base_str == "冰" or base_str == "Ice":
                if extra_ingredient == "Pizza" or extra_ingredient == "披薩":
                    return 0, "Error: Ice cannot add pizza"
            # get extra price and add it in total
            ep, ep_error_message = extra_price_inte(
                product_str, extra_ingredient, odoo_standard=False
            )
            if ep_error_message == None:
                # print(f"extra_ingredient = {extra_ingredient}, ep = {ep}")
                total_price += ep * extra_quantity
            else:
                return 0, ep_error_message
        else:
            return 0, "Error: Extra undefined Extra or NOT acceptable combinations"

    # correct return
    return total_price, error_message
    #################33 unit test


def price_function_unit_test():
    """Part I: testing extra_price in total_price calculation
    Part II: testing the extra_price fucntion directly"""
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
            "Peanut Mango Pizza + Ice",
            250 + 0,
        ),
        (
            "花生 冰 + 巧克力",
            "Peanut Icd + Chocolate",
            70,
        ),
        ("", "", "Nothing selected"),
    ]
    # part I tests: total price (using extra pricing)
    for name, e_name, msg_or_price in menu_item_names:
        total_price, error_message = total_price_inte(name)
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

    # part II test: extra price fucntion directly

    extra_price_items = [  # product_str, extra_ingredient, extra_ingredient_english, correct extra price/error message,
        ("花生 芒果 披薩", "冰", "Ice", 0),
        ("花生 芒果 披薩", "優格", "Yogurt", 7),
        ("花生 芒果 披薩", "披薩", "Pizza", 8),
        ("花生 芒果 披薩", "花生", "Peanut", 5),
        ("花生 芒果 披薩", "芒果", "Mango", 15),
        ("花生 芒果 披薩", "巧克力", "Chocolate", 5),
        ###############
        ("花生 冰", "冰", "Ice", 0),
        ("花生 冰", "優格", "Yogurt", 7),
        ("花生 冰", "披薩", "Pizza", 8),
        ("花生 冰", "花生", "Peanut", 10),
        ("花生 冰", "芒果", "Mango", 15),
        ("花生 冰", "巧克力", "Chocolate", 10),
        #############
        ("花生 芒果 巧克力 優格", "冰", "Ice", 0),
        ("花生 芒果 巧克力 優格", "優格", "Yogurt", 7),
        ("花生 芒果 巧克力 優格", "披薩", "Pizza", 8),
        ("花生 芒果 巧克力 優格", "花生", "Peanut", 5),
        ("花生 芒果 巧克力 優格", "芒果", "Mango", 15),
        ("花生 芒果 巧克力 優格", "巧克力", "Chocolate", 5),
        ########### odoo standard product
        ("odoo standard product", "冰", "Ice", 0),
        ("odoo standard product", "優格", "Yogurt", 7),
        ("odoo standard product", "披薩", "Pizza", 8),
        ("odoo standard product", "花生", "Peanut", 5),
        ("odoo standard product", "芒果", "Mango", 15),
        ("odoo standard product", "巧克力", "Chocolate", 5),
    ]
    for product_str, extra_ingr, extra_ingr_en, extra_price in extra_price_items:
        if product_str == "odoo standard product":
            ep, error_message = extra_price_inte(
                product_str, extra_ingr, odoo_standard=True
            )
        else:
            ep, error_message = extra_price_inte(product_str, extra_ingr)
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
                print(
                    f"correct result  --->  DCP {name}, extra {extra_ingr} extra price is {ep}"
                )

        else:
            print(f"error message: {error_message}")
    # speacial tests for debugging
    price, error_string = extra_price_inte("花生 冰", "巧克力")
    print(f"price = {price}, error = {error_string}")


if __name__ == "__main__":
    try:
        price_function_unit_test()

    except Exception as e:
        print_error(e)
else:
    pass
