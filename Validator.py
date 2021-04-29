from configs.functionalities import functionalities
from configs.bcolors import bcolors
colors = bcolors()

class Validator:
    def __init__(self, obj):
        obj = self.exclude_unimportant(obj)
        keys = obj.keys()
        self.valid_starters = list(   map(lambda x: x['starter'], functionalities.values())  )
        self.valid_starters = list(  filter(lambda x: x in keys , self.valid_starters)   )
        if not self.count_Trues(obj):
            exit
        combination = filter(lambda x: x['starter'] in keys,functionalities.values())
        combination = list(combination)
        if len(combination) < 1:
            raise Exception('No option selected!')

        if len(combination) > 1:
            raise Exception('Too many options selected!')
        combination = combination[0]
        
        keys = combination.keys()
        supported = []
        
        for key in keys:
            if type(combination[key]) == list:
                supported += combination[key]
            else:
                supported +=  [combination[key]]
        
        for key in obj.keys():
            if key not in supported:
                raise Exception(f'The argument {colors.WARNING}{key}{colors.ENDC} is not supported in this function.')
        
        
        if 'required' in keys:
            if not self.required(obj,combination['required']):
                raise Exception(f"This function requires {colors.OKBLUE}ALL{colors.ENDC} of the following parameters: {colors.OKGREEN}{combination['required']}{colors.ENDC}.")
        
        if 'at_least' in keys:
            if not self.at_least(obj,combination['at_least']):
                 raise Exception(f"This function requires {colors.OKBLUE}AT LEAST{colors.ENDC} one of the following parameters:{colors.OKGREEN}{combination['at_least']}{colors.ENDC}.")
        
        self.obj = obj
        self.combination = combination
        
        
        

    def exclude_unimportant(self,obj):
        return {tag: obj[tag] for tag in obj.keys() if obj[tag]}
    
    def count_Trues(self,obj):
        count = 0
        for tag in self.valid_starters:
            if obj[tag] == True:
                count += 1
        
        if count < 1:
            raise Exception('Not enough arguments passed!')
            return False
        elif count > 1:
            raise Exception('Too many arguments passed!')
            return False

        return True
    
    def required(self,obj,arr):
        keys = obj.keys()
        for key in arr:
            if key not in keys:
                return False
        
        return True
        
    def at_least(self,obj,arr):
        keys = obj.keys()
        for key in arr:
            if key in keys:
                return True

        return False

    def get_params(self):
        obj = dict(self.obj)

        del obj[self.combination['starter']]
        return {
            'starter': self.combination['starter'],
            'params': obj
        }
    