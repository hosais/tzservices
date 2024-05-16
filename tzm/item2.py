# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com


from tzm import base
from tzm.tzdb import DataComponent, DbDataCo, mdb

from pymongo import IndexModel, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from tzm.base import print_error
import copy
import re


# menually keyinjson format for menu
# create validator
# price calculator validator for input string (product name)
# item1 item2 item3 base1 + addon_productx1  -> price


# pair elements definitions in base pair (INGREDIENT_NAME,BASE_PRICE,EXTRA_PRICE  )
INGREDIENT_NAME = 0  # ingredient name
BASE_PRICE = 1
INGR_PRICE_INDEX = 2 # index of ingredient base price for different bases 
INGR_PRICES = 1
BASE_EXTRA_PRICE = 3
INGR_EXTRA_PRICE = 2
BASE_RULE= 4
INGR_RULE = 3  


class MenuInfo(DataComponent):
    """
    Menu Info: The real Data settings for BASEs and INGREDIENTS (such as tamplate table of all ingredients)
    BASE part is class attribute because it is only one data

    Ingredients will have many different version depends on BASE so it is instance level

    """

    menu_base = {
        "base": [  # (name, base_price, ingredient_price_index,default_extra_price,rules)
            ("豆花",        40, 1, 5, "max65"),
            ("湯",          40, 1, 5, "max65"),
            ("巧克力布丁",   45, 2, 5, "max70"),
            ("牛奶布丁",     45, 2, 5, "max70"),
            ("布丁",         45, 2, 5, "max70"),
            ("仙草凍",       45, 2, 3, 5, "max70"),
            ("鮮奶仙草凍",    55, 3, 5, "max85"),
            ("燒仙草",       45, 2, 5, "max65"),
            ("牛奶冰",       60, 4, 10, "max85"),
            ("圓湯(自選)",    80, 5, 5, "max80"),
        ]
    }

    # Create ingredients according to code
    menu_ingredients = {
        "ingredients_nature": [  # (name, ingredient_first_prices (tuple, different prces based on different bases), rules, special_extra)
            ("紅豆", (10,10)),
            ("綠豆", (10,10)),
            ("花生", (15,10)),
            ("薏仁", (10,10)),
            ("麥角", (10,10)),
            ("花豆", (10,10)),
            ("銀耳", (15),  "if_coix_yiner"      ),
        ],
        "ingredients_QQ": [  # (name, ingredient_first_price, extra price,rule)
            ("珍珠粉圓", (5,10), None, "if_qq_combo"),
            ("涼圓", (5,10), None, "if_qq_combo"),
            ("芋圓", (20,10), None, "if_taro_combo, if_qq_combo"),
            ("地瓜圓", (20,10), None, "if_taro_combo, if_qq_combo"),
            ("黑糖粉粿", (15,10), None, "if_taro_combo, if_qq_combo"),
            ("綜合圓", (15,10)),
            ("QQ", (10,10), 10),
        ],
        "ingredients_Fruits": [  # (name, ingredient_first_price, extra price,rule)
            ("芒果", (25,10)),
            ("西瓜", (25,10)),
            ("鳳梨", (25,10)),
            ("奇異果", (25,10)),
        ],
        "default_rule": "max 55",
    }

    def __init__(self, dict_obj=None, isCopy=True):
        try:
            # get default data from _model_fields  (self.data = _model_fields)
            super().__init__(dict_obj, isCopy)
            # do customized thing here
            if not self.validate_ingredients_uniqueness():
                raise ValueError("ingredients names must be unique")

        except Exception as e:
            # from tzm.base import print_error
            print_error(e)

    ###### BASIC OPERATION #######
    @classmethod
    def search_pair_in_list(cls, pair_list, item_name):
        """
        return None if not found
        """
        for p in pair_list:
            if p[0] == item_name:
                # first element in pair to be the search key
                return p
        return None

    @classmethod
    def ing_has_extra_price(cls, ing_pair, ingredient=True):
        '''
        check if there is setting for the ingredient that has ingredient extra price 
        '''
        if ingredient:
            if len(ing_pair) > INGR_EXTRA_PRICE:
                if type(ing_pair[INGR_EXTRA_PRICE]) is type (1):
                    return True 

        return False


    ############## retrive all data ####################
    @classmethod
    def get_all_bases(cls):
        all_bases = []
        for pair in cls.menu_base["base"]:
            all_base.append(pair[INGREDIENT_NAME])
        return all_bases

    @classmethod
    def get_all_base_pairs(cls):
        return cls.menu_base["base"]

    @classmethod
    def get_all_ingredient_pairs(cls, group=None):
        """
        return all ingredients if no group parameter
        return specific group of ingredient if the group != None
        """
        if group == None:
            # all ingredients
            ingredient_list = (
                cls.menu_ingredients["ingredients_nature"]
                + cls.menu_ingredients["ingredients_QQ"]
                + cls.menu_ingredients["ingredients_Fruits"]
            )
        else:
            ingredient_list = cls.menu_ingredients[group]
        return ingredient_list

    ############## retrive data ####################
    @classmethod
    def get_base_rules(cls,base_name):
        all_bases = []
        for pair in cls.menu_base["base"]:
            all_base.append(pair[INGREDIENT_NAME])
        return all_bases
    @classmethod
    def get_base_index_for_ingredeint_pair(cls, base_name):
        """
        get base index.  The index can be used to access the ingredient price for that specfic base
        For example, Red bean price for DOUHUA is 10 but for ICE maybe 5

        """
        base_pair = MenuInfo.get_base_pair(base_name)
        if base_pair == None:
            raise ValueError("base cannot found")
        return base_pair[INGR_PRICE_INDEX]

    ############# get pair by base, ingredient
    @classmethod
    def get_base_pair(cls, base_name):
        base_list = cls.get_all_base_pairs()
        result = cls.search_pair_in_list(base_list, base_name)
        if result == None:
            raise ValueError("base cannot found")
        return result

    @classmethod
    def get_ingredient_pair(cls, ingredient_name):
        result = None
        all_ingredient_list = cls.get_all_ingredient_pairs()
        # using class fucntion (not type casting here)
        result = cls.search_pair_in_list(all_ingredient_list, ingredient_name)
        # if found, result will return later

        return result  # return pair or None

    @classmethod
    def get_base_default_extra_price(cls, base_name):
        """
        every base has its default extra price
        """
        if type(base_name) is not str:
            raise ValueError("base_name should not be a empty list")
            
        base_pair = MenuInfo.get_base_pair(base_name)
        return base_pair[BASE_EXTRA_PRICE]
    @classmethod
    def get_ingredient_extra_price(cls, ingredient_name,base_name):
        '''
            get extra price from ingredient, if does not have, return base default extra price
        '''
        ingredient_pair = MenuInfo.get_ingredient_pair(ingredient_name)
        if ingredient_pair == None:
            print(f"ingredient_name = {ingredient_name}")
            raise ValueError("ingredient cannot found")
        
        if MenuInfo.ing_has_extra_price(ingredient_pair):
            #print(f"ingredient_pair[INGR_EXTRA_PRICE] = {ingredient_pair[INGR_EXTRA_PRICE]}")
            return ingredient_pair[INGR_EXTRA_PRICE]
        else:            
            # ingredient pair does not have extra price"
            #print(f"!!!extra price = {MenuInfo.get_base_default_extra_price(base_name)} ")
            return MenuInfo.get_base_default_extra_price(base_name)
        
        

    @classmethod
    def get_price_of_ingredient_for_base(cls, ingredient_name, base_name):
        ingredient_pair = MenuInfo.get_ingredient_pair(ingredient_name)
        if ingredient_pair == None:
            print(f"ingredient_name = {ingredient_name}")
            raise ValueError("ingredient cannot found")
        ind = MenuInfo.get_base_index_for_ingredeint_pair(base_name)
        print(f"pair = ingredient {ingredient_pair}")
        print(f"ind, INGR_PRICES = {ind} {INGR_PRICES}")
        # need to make sure the ind exisits ERROR CHeck need to do
        price = ingredient_pair[INGR_PRICES][ind]
        return price
    

    @classmethod
    def validate_ingredients_uniqueness(cls):
        """
        the ingredient names must be unique
        """
        ing_list = cls.get_all_ingredient_pairs()
        name_list = []
        for ing_pair in ing_list:
            # get the names of the ingredient from the ingredient info (pair)
            name_list.append(ing_pair[0])
        return len(name_list) == len(set(name_list))


# currently MenuInfo does have instance variables so all data is class variables
# just in case in the future instance is needed, still we use instance variable
menu_info_v = MenuInfo()
#


class ModifierItem(DataComponent):
    """
    One ingredient record (price ... etc)
    This is the modifier structure that is based on the data in menuinfo

    """

    _model_fields = {
        "item_name": "",
        "default_quantity": 1,
        "base_price": 0,
        "extra_price": None,  # None-> not used in default
        "rules": "max55",
    }

    def __init__(self, dict_obj=None, isCopy=True):
        super().__init__(dict_obj, isCopy)
        self.menu_info = None

    def set_menu_info(self, menu_info):
        self.menu_info = menu_info

    def construct_md_item_by_name(self, ingredient_name):
        """
        create_ingredient_item() will create modifier item refer to the menu info
        Need to call set_menu_info() first
        Extra price is not used in normal case. (== None)
        """

        self.setField("item_name", ingredient_name)
        self.setField("default_quantity", 1)
        if self.menu_info == None:
            raise AttributeError("to create modifier, it needs menu_info to refer to")
        i_pair = MenuInfo.get_ingredient_pair(ingredient_name)
        # ingredient base_price

        self.setField("base_price", i_pair[BASE_PRICE])
        # extra_price
        if len(i_pair) >= 3:  # if there is extra price
            self.setField("extra_price", i_pair[EXTRA_PRICE])
        else:
            self.setField("extra_price", None)
        if len(i_pair) >= 4:
            self.setField("rule", i_pair[RULE])
        else:
            self.setField("rule", None)
        return self.data

    def search_by_name_of_md_list(modifier_item_list, name):
        for mdl in modifier_item_list:
            if mdl.getField("item_name") == name:
                return mdl


class MenuItem(DbDataCo):
    """
    respresent a DCProduct
    """

    ################### begin col ##########################################33
    # __qualname__ == class name and will NOT inherit from base class => every DataComponent child needs to have these two lines
    col_name = __qualname__
    col = mdb.get_db()[__qualname__]
    #################### end col ############################################
    # model fields can be check and accessed if needed by self.model_fields but it is readonly

    _model_fields = {
        # product item
        "type": "extended",
        "name": "紅豆黑糖粉粿湯",
        "name_en": "Douhua with Green Bean",
        "pic_url": "https://www.shaadidukaan.com/vogue/wp-content/uploads/2019/08/hug-kiss-images.jpg",
        "description": "food  description ",
        "sold_its_own": True,
        "categories": [],
        "price": 40,
        "cprice": True,
        "specail_price": {10, "when it is in another menu"},
        "sell_time": "Menu1",  # can be based on menu availabe time"
        "out_of_stock": False,
        "defaul_temp": "Heated",  # default temperature
        "dietary attributes": "Vegetarian",
        "customize_items": [],  # Modifier groups allow customers to use toppings, sides and more to customize items
        "item_list": "紅豆 黑糖粉粿 湯",  # base would be the last  string.split ==> words list
        # 　to get the last item:　(data["item_list"].split)[-1]
    }
    # product item Ex: 紅豆黑糖粉粿湯
    # base item Ex: 豆花
    # ingredient Ex:

    _db_index_list = [IndexModel([("name", DESCENDING)], unique=True)]
    # For index definition,
    # refer to https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index

    # Use DataComponent __init__ Or override __init__:
    # if dict_obj is none, _model_fields will be copy to self.data
    # you can override __init__ like following
    def __init__(self, dict_obj=None, isCopy=True):
        try:
            # get default data from _model_fields  (self.data = _model_fields)
            super().__init__(dict_obj, isCopy)
            # do customized thing here
            self.data["test"] = "unitest is great!"

        except Exception as e:
            # from tzm.base import print_error
            print_error(e)

    def add_modifier(self, modifier):
        self.getField("customize_items").append(modifier.getField("name"))


class Menu:
    modifier_template = {
        "name": "豆花配料",
        "description": "",
        "is_default_quantity": False,
        "default_extra_price": 5,  # 5 for douhua extra default
        "items": [
            # {
            # "item_name" = "綠豆",
            # "default_quantity":1,
            # "extra_price":5,
            # "base_price":10,
            # "rule":"Max55"
            # },
        ],
    }

    item_template = {
        # product item
        "type": "extended",
        "name": "豆花",
        "name_en": "Douhua with Green Bean",
        "pic_url": "https://www.shaadidukaan.com/vogue/wp-content/uploads/2019/08/hug-kiss-images.jpg",
        "description": "food  description ",
        "sold_its_own": True,
        "categories": [],
        "price": 40,
        "cprice": True,
        "specail_price": {10, "when it is in another menu"},
        "sell_time": "Menu1",  # can be based on menu availabe time"
        "out_of_stock": False,
        "defaul_temp": "Heated",  # default temperature
        "dietary attributes": "Vegetarian",
        "customize_items": [],  # Modifier groups allow customers to use toppings, sides and more to customize items
        "item_list": "",  # base would be the last  string.split ==> words list
        # 　to get the last item:　(data["item_list"].split)[-1]
    }
    # consturct each product with item_list
    # self learning menu?
    # most recent order products

    def __init__(self):
        pass
        # generate menu

    # rule functions
    @classmethod
    def rule_paras_list(cls, rule_str):
        print(rule_str)
        return rule_str.split()

    def get_all_rules(modifier_list):
        """ """
        pass

    def r_max(price_max_value, price):
        if price > price_max_value:
            return price_max_value
        else:
            return price

    def calculate_price(self, product_item_string):
        """
        the inner function will access the parameter directly (side effect may be there)
        """

        def get_base(product_item_list):
            """
            This would remove the base item in the product_item_list
            return base_price, base_str
            """
            # ------------- BASE price
            # remove the base (last one)
            base_str = product_item_list.pop()  # get the last (default index = -1)
            # get base price
            base_pair = MenuInfo.get_base_pair(base_str)
            base_price = base_pair[BASE_PRICE]
            return base_price, base_str

        def get_max_ingredient_base_price(product_item_list, base_name):
            """
            this will remove the max base item in product_item_list
            return ing_base_price
            """
            if product_item_list == []:
                raise ValueError("ingredient_base should not be a empty list")

            # ------------- ING BASE price
            # get first ingredients price
            # find the ingredient base price

            ing_base_price = 0
            ing_base_str = ""

            ingredeint_list_dup = copy.deepcopy(product_item_list)
            while ingredeint_list_dup != []:
                # find max price
                new_ing_base_str = ingredeint_list_dup.pop(0)
                # pop from the first item in general. If the price is the same, QQ would be the later and will be selected as extra (+10)
                ingr_price = MenuInfo.get_price_of_ingredient_for_base(
                    new_ing_base_str, base_name
                )
                if ingr_price > ing_base_price:
                    # print(f"mi in max_Base selected= {modifier_item.data}")
                    ing_base_price = ingr_price
                    ing_base_str = new_ing_base_str

            # The result => ing_base_str, ing_base_price, modifier_item

            #     # remove the ing_base_price item

            product_item_list.remove(ing_base_str)
            return ing_base_price

        def get_other_ingredient_price(product_item_list, base_name):
            """
            besides of main ingredient_price, 
            return the price of the sum of the other ingredients

            """
            if product_item_list == []:
                raise ValueError("ingredient_base should not be a empty list")

            ingredient_price = 0
            for product_str in product_item_list:
                extra_ing_price = MenuInfo.get_ingredient_extra_price(product_str,base_name)
                
                print(f"ingredient_price {ingredient_price}  += extra_ing_price {extra_ing_price}")
                ingredient_price += extra_ing_price

            return ingredient_price

        def get_extra_price(extra_item_list, base_name):
            """
            return extra_price  # customers add extra things
            extra_item_list is a no space extra string list ("+ING*2+ING2*3 ...")
            """

            all_extra_price = 0
            for extra_str in extra_item_list:
                # pasing one extra_str
                integredient_and_quantity = extra_str.split("*")
                extra_ingredient = integredient_and_quantity[0]
                # get extra price from all item
                extra_price = MenuInfo.get_ingredient_extra_price(extra_ingredient,base_name)
                
                # get extra quantity
                if len(integredient_and_quantity) == 2:
                    extra_quantity = int(integredient_and_quantity[1], base=10)
                else:
                    extra_quantity = 1  # no "x #" = > default value =1
                all_extra_price += extra_price * extra_quantity
            # print(f"all extra price ={all_extra_price} ")
            return all_extra_price

        def get_all_rules(product_item_list):
            """
            need to return all rule list in the ingredient list with no duplicate
            """
            rule_str_list = []
            for item_name in product_item_list:
                #rule_str = modifier_item.getField("rule")
                rule_str = "Not coding yet"
                rule_str_list.append(rule_str)
            return rule_str_list

        def r_max(all_rule_list, t_price):
            has_max_rule = False
            for rule_str in all_rule_list:
                # exist max rule
                print("LINE 501")
                print(rule_str)
                rule_list = Menu.rule_paras_list(rule_str)
                if "max" in rule_list:
                    if has_max_rule == True:
                        raise ValueError("Max rule can be only one")
                    has_max_rule = True
                    max_price = int(rule_list[1])

                    if t_price > max_price:
                        t_price = max_price
                    return t_price

        ########## calculate_price() main code start  #################33

        total_price = 0

        #################### Get elements

        if (product_item_string) != str:
            error_message = "prodcut_str is not a string"

        ########################### take out extra part, with '+' symbol
        # replace group ingredients (combo for example)

        # take parts with the symbol '+'
        extra_symbol = "\+"  # extra  for regex string requirement
        parts = re.split(
            extra_symbol, product_item_string
        )  # parts should be "ingredient" or "ingredient * #" forms.

        dpc = 0  # dynamic product combination
        dpc_str_temp = parts.pop(dpc)
        # take the first string before '+' => not extra ingr
        dpc_str = dpc_str_temp.strip()  #  <<---- to see there are easier way?
        ingredient_list = dpc_str.split()
        # Note: string split() also remove space characters

        ############## preparing extra ingredients
        # after pop() parts have only extra
        no_space_extras = [x.replace(" ", "") for x in parts]

        # print(f"extra = {no_space_extras}")

        ##################
        # check combo rules
        # if_taro_combo if_qq_combo -> need to replace related to taro_combo or qq_combo
        # replace related items to combo
        # need add rule functions herer!!!!!!!!!!!!!!!!!!!


        # Base price
        base_price, base_str = get_base(ingredient_list)
        total_price += base_price
        print(f"base price={total_price}")

        ####################   <---- adding total price  BASE PRICE
        ### preparing menu item
        ################################
        # check all rules
        if ingredient_list != []:
            all_rule_list = get_all_rules(ingredient_list)

        # if only base, ingredient_list would be []
        if ingredient_list != []:
            total_price += get_max_ingredient_base_price(ingredient_list, base_str)
            print(f"add max ingredient, total={total_price}")
            ###############   <---- adding total price  ING BASE PRICE
        if ingredient_list != []:
            total_price += get_other_ingredient_price(ingredient_list, base_str)
            print(f"add other ingredients={total_price}")

    ###take care the the MAX rule here !!!!!!!!!!!!!!1


        # process the rest extra elements
        total_price += get_extra_price(no_space_extras, base_str)
        print(f"add extra ingredients, total={total_price}")
        ## check max55 rule
        # if price is higher than 55, it becomes 55
        # total_price = r_max(all_rule_list, total_price)

        # get add_on price
        # sum the total price
        return total_price, error_message


def unit_test_item():
    try:
        my_menu = Menu()
        menu_item_names = [
            ("豆花", 40),
            ("珍珠粉圓 豆花", 45),
            ("黑糖粉粿 豆花", 55),
            ("QQ 豆花", 50),
            ("綜合圓 豆花", 55),
            ("QQ 花生 豆花", 65),
            (
                "綠豆 QQ 豆花",
                60,
            ),  # <-- need to take care QQ + 10 rule => change the string before get into calculation
            (
                "黑糖粉粿 綜合圓 豆花",
                60,
            ),  # <-- need take care of special combination promotion => refused, need to click promotion item
            (
                "芋圓 地瓜圓 豆花",
                55,
            ),  # <-- need to check the combination of group such as QQ=xxx,xxx,xxx,xxx, 綜合圓=芋圓 地瓜圓
            ("豆花 + QQ * 2", 60),
        ]

        for name, price in menu_item_names:
            p_price, error_message = my_menu.calculate_price(name)
            if p_price != price:
                print(f"!!!!!!!!!!!!!!test failed:  product_name={name}")
                print(f"price = {p_price} should be {price}")

        # rule need to impl
        # different base table
        # error_message

    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    unit_test_item()
else:
    pass
