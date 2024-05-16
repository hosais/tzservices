# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com

''' ***********   Rule functions ***********
       Rule function can be few types: 
           1) special group ingredient (3Q, taro balls  ...)
           2) max_type (less than ...)
           3) more to be updated


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
            


        

 

        
########## calculate_price() main code start  #################33
        



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
    
    

if __name__ == "__main__":
    unit_test_price_rule()
else:
    pass
