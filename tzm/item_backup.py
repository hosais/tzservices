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
INGREDIENT_PRICE_INDEX = 2
EXTRA_PRICE = 3
RULE = 4  # after 4


class MenuInfo(DataComponent):
    """
    Menu Info: The real Data settings for BASEs and INGREDIENTS (such as tamplate table of all ingredients)
    BASE part is class attribute because it is only one data

    Ingredients will have many different version depends on BASE so it is instance level

    """

    menu_base = {
        "base": [  # (name, base_price, ingredient_price_index,default_extra_price,rules)
            ("豆花", 40, 1, 5, "max65"),
            ("湯", 40, 1, 5, "max65"),
            ("巧克力布丁", 45, 2, 5, "max70"),
            ("牛奶布丁", 45, 2, 5, "max70"),
            ("布丁", 45, 2, 5, "max70"),
            ("仙草凍", 45, 2, 3, 5, "max70"),
            ("鮮奶仙草凍", 55, 3, 5, "max85"),
            ("燒仙草", 45, 4, 5, "max65"),
            ("牛奶冰", 60, 5, 10, "max85"),
            ("圓湯(自選)", 80, 6, 5, "max80"),
        ]
    }

    # Create ingredients according to code
    menu_ingredients = {
        "ingredients_nature": [  # (name, ingredient_first_price, rules)
            ("紅豆", 10),
            ("綠豆", 10),
            ("花生", 15),
            ("薏仁", 10),
            ("麥角", 10),
            ("花豆", 10),
            (
                "銀耳",
                15,
                "if_coix_yiner",
            ),
        ],
        "ingredients_QQ": [  # (name, ingredient_first_price, extra price,rule)
            ("珍珠粉圓", 5, None, "if_qq_combo"),
            ("涼圓", 5, None, "if_qq_combo"),
            ("芋圓", 20, None, "if_taro_combo, if_qq_combo"),
            ("地瓜圓", 20, None, "if_taro_combo, if_qq_combo"),
            ("黑糖粉粿", 15, None, "if_taro_combo, if_qq_combo"),
            ("綜合圓", 15),
            ("QQ", 10, 10),
        ],
        "ingredients_Fruits": [  # (name, ingredient_first_price, extra price,rule)
            ("芒果", 25),
            ("西瓜", 25),
            ("鳳梨", 25),
            ("奇異果", 25),
        ],
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

    @classmethod
    def search_pair_in_list(cls, pair_list, item_name):
        """
        return None if not found
        """
        for p in pair_list:
            print(f"p={p}, item_name = {item_name}")
            if p[0] == item_name:
                # first element in pair to be the search key
                return p
        return None

    @classmethod
    def is_has_extra_price(pair):
        return len(pair) >= EXTRA_PRICE

    # be able to search
    @classmethod
    def get_base_pair(cls, base_name):
        base_list = cls.menu_base["base"]
        result = cls.search_pair_in_list(base_list, base_name)
        if result == None:
            raise ValueError("base cannot found")

    @classmethod
    def get_base_default_extra_price(cls, base_name):
        """
        every base has its default extra price
        """
        if type(base_name) is not str:
            raise ValueError("ingredient_base should not be a empty list")

        base_pair = MenuInfo.get_base_pair(base_name)
        print(f"base_pair = {base_pair}")
        return base_pair[EXTRA_PRICE]

    @classmethod
    def get_ingredient_pair(cls, ingredient_name):
        result = None
        all_ingredient_list = (
            cls.menu_ingredients["ingredients_nature"]
            + cls.menu_ingredients["ingredients_QQ"]
            + cls.menu_ingredients["ingredients_Fruits"]
        )
        # using class fucntion (not type casting here)
        result = cls.search_pair_in_list(all_ingredient_list, ingredient_name)
        # if found, result will return later

        return result  # return pair or None

    @classmethod
    def get_all_bases(cls, group=None):
        all_bases = []
        for pair in cls.menu_base["base"]:
            all_base.append(pair[INGREDIENT_NAME])
        return all_bases

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


class BaseModifers(DbDataCo):
    """
    DbDataCo <= binding to database (Mongodb)
    The database name is the class name
    =====================================
    Each base supposely has a set of Menu modififers. these modifiers are colected in one BaseModifers
    EX: douhua Menu that include a list of modifiers (ModifierItems)
    """

    ################### begin col ##########################################33
    # __qualname__ == class name and will NOT inherit from base class => every datacomponent child needs to have these two lines
    col_name = __qualname__
    col = mdb.get_db()[__qualname__]
    #################### end col ############################################
    # model fields can be check and accessed if needed by self.model_fields but it is readonly

    _model_fields = {
        "name": "豆花",  # base name
        "description": "",
        "is_default_quantity": False,
        "default_extra_price": 5,  # 5 for douhua extra default
        "items": [  # a list of modifier items
            # {
            # "item_name" = "綠豆",
            # "default_quantity":1,
            # "extra_price":5,
            # "base_price":10,
            # "rule":"Max55"
            # },
        ],
    }

    _db_index_list = [IndexModel([("name", DESCENDING)], unique=True)]
    # For index definition,
    # refer to https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index

    # Use DataComponent __init__ Or override __init__:
    # if dict_obj is none, _model_fields will be copy to self.data
    # you can override __init__ like following

    def __init__(self, base_name=None, dict_obj=None, menu_info=None, isCopy=True):
        try:
            if menu_info == None:
                raise AttributeError("BaseModifers need menu_info to refer to")
            if base_name == None:
                raise AttributeError("BaseModifers need base_name to refer to")

            # get default data from _model_fields  (self.data = _model_fields)
            super().__init__(dict_obj, isCopy)
            # do customized thing here
            self.menu_info = menu_info
            self.setField("name", base_name)
            self.setField(
                "default_extra_price", MenuInfo.get_base_default_extra_price(base_name)
            )
        except Exception as e:
            # from tzm.base import print_error
            print_error(e)

    def add_item(self, modifier_item):
        """
        add item (dictionary form) to the modifier_item list
        """
        self.getField("items").append(modifier_item.getData())

    def add_all_menu_items(self):
        for ingredient_pair in self.menu_info.get_all_ingredient_pairs():
            md = ModifierItem()
            md.set_menu_info(self.menu_info)
            md.construct_md_item_by_name(ingredient_pair[INGREDIENT_NAME])
            self.add_item(md)

    def get_mi_by_name(self, item_name):
        """
        get modifier item by name
        """
        for item in self.getField("items"):
            if item["item_name"] == item_name:
                mi = ModifierItem(dict_obj=item)
                mi.set_menu_info(self.menu_info)
                return mi
        return None

    def search_in_items(self, item_name):
        def match_item_name(item, **kwargs):
            if item["item_name"] == kwargs["item_name"]:
                return True
            else:
                return False

        return self.searchListField("items", match_item_name, item_name=item_name)


class MenuItem(DbDataCo):
    """
    respresent a DCProduct
    dynamnic combination product
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

        # generate menu
        all_bases = MenuInfo.get_all_bases()
        self.menu_modifiers = []

        for base in all_bases:
            menu_modifier = BaseModifers(
                base_name=base, dict_obj=self.modifier_template, menu_info=menu_info_v
            )
            menu_modifier.add_all_menu_items()

            self.menu_modifiers.append((base, menu_modifier))

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

    def find_modifier(self, modifier_name):
        md_list = self.menu_modifiers
        for md in md_list:
            if md.getField("name") == modifier_name:
                return md

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
            base_price = base_pair[1]
            return base_price, base_str

        def get_max_ingredient_base_price(product_item_list, base_modifiers):
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
                modifier_item = base_modifiers.get_mi_by_name(new_ing_base_str)
                if modifier_item.getField("base_price") > ing_base_price:
                    # print(f"mi in max_Base selected= {modifier_item.data}")
                    ing_base_price = modifier_item.getField("base_price")
                    ing_base_str = new_ing_base_str

            # The result => ing_base_str, ing_base_price, modifier_item

            #     # remove the ing_base_price item

            product_item_list.remove(ing_base_str)
            return ing_base_price

        def get_other_ingredient_price(product_item_list, base_modifiers):
            """
            return ingredient_price

            """
            if product_item_list == []:
                raise ValueError("ingredient_base should not be a empty list")

            ingredient_price = 0
            for product_str in product_item_list:
                modifier_item = base_modifiers.get_mi_by_name(product_str)
                # print(f"mi = {modifier_item.data}")
                if modifier_item.getField("extra_price") != None:
                    extra_price = modifier_item.getField("extra_price")
                else:
                    extra_price = md.getField("default_extra_price")
                ingredient_price += extra_price

            return ingredient_price

        def get_extra_price(extra_item_list, base_modifiers):
            """
            return extra_price
            extra_item_list is a no space extra string list ("ING*2,ING2*3 ...)
            """

            all_extra_price = 0
            for extra_str in extra_item_list:
                # pasing one extra_str
                integredient_and_quantity = extra_str.split("*")
                extra_ingredient = integredient_and_quantity[0]
                # get extra price from all item
                modifier_item = base_modifiers.get_mi_by_name(extra_ingredient)
                if modifier_item.getField("extra_price") != None:
                    extra_price = modifier_item.getField("extra_price")
                else:
                    extra_price = md.getField("default_extra_price")
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
                modifier_item = md.get_mi_by_name(item_name)
                rule_str = modifier_item.getField("rule")
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
        # Base price
        base_price, base_str = get_base(ingredient_list)
        total_price += base_price
        print(f"base price={total_price}")

        ####################   <---- adding total price  BASE PRICE
        ### preparing menu item
        # get the menu item with the base
        menu_item = MenuItem[base_str]
        customized_list = menu_item.getField(
            "customize_items"
        )  # <-- customized_menu_items are modifier name list
        # the product string need to have ingredients, currently only one is support
        # in the future, could give some parameter for get which modifier if there are more than one
        md = self.find_modifier(customized_list[0])
        # md is for using in the following sub-methods
        ################################
        # check all rules
        if ingredient_list != []:
            all_rule_list = get_all_rules(ingredient_list)

        # if only base, ingredient_list would be []
        if ingredient_list != []:
            total_price += get_max_ingredient_base_price(ingredient_list, md)
            print(f"add max ingredient, total={total_price}")
            ###############   <---- adding total price  ING BASE PRICE
        if ingredient_list != []:
            total_price += get_other_ingredient_price(ingredient_list, md)
            print(f"add other ingredients={total_price}")
        # process the rest extra elements
        total_price += get_extra_price(no_space_extras, md)
        print(f"add extra ingredients, total={total_price}")
        ## check max55 rule
        # if price is higher than 55, it becomes 55
        # total_price = r_max(all_rule_list, total_price)

        # get add_on price
        # sum the total price
        return error_message, total_price


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
            p_price = my_menu.calculate_price(name)
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
