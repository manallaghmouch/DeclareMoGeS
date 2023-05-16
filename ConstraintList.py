from Constraint import *
from black_sat import *
import re

class ConstraintList(list):
    """This class creates a list of constraints"""
    
    def check_if_exists(self, x, ls):
        if x in ls:
            return True
        else:
            return False 

    # Check for dependencies 
    def contains_constraint(self, constraint, constraint_list):
        if constraint == None: 
            return True
        else:
            constraint_list_str = [str(x) for x in constraint_list]
            match constraint.__class__.__name__:
                # templates that can only occur once in the model
                case 'Init':
                    startswith_ls = [x.startswith('Init') for x in constraint_list_str]
                    return ConstraintList.check_if_exists(self, True, startswith_ls)
                case 'End':
                    startswith_ls = [x.startswith('End') for x in constraint_list_str]
                    return ConstraintList.check_if_exists(self, True, startswith_ls)               
                case _: return False

    def list_to_decl_extension(self, constraint_list, activities):
        output_activities = ""
        output_constraints = ""

        # activities
        for item in activities:
            item_str = "activity " + str(item) + "\n"
            output_activities += item_str

        output1 = ""
        output2 = ""

        for item in constraint_list[:-1]:
            item_str = str(item) + " | | |\n"
            item_str = item_str.replace("(","[")
            item_str = item_str.replace(")","]")
            item_str = item_str.replace(",",", ")
            item_split = re.findall('[A-Z][^A-Z]*', item_str)
            item_str = " ".join(str(item) for item in item_split)
            output1 += item_str

        # last item constraint_list
        item_last_str = str(constraint_list[len(constraint_list)-1]) + " | |"
        item_last_str = item_last_str.replace("(","[")
        item_last_str = item_last_str.replace(")","]")
        item_last_str = item_last_str.replace(",",", ")
        item_split = re.findall('[A-Z][^A-Z]*', item_last_str)
        item_last_str = " ".join(str(item) for item in item_split)
        output2 = item_last_str

        output_constraints = output1 + output2

        output = output_activities + output_constraints

        return output
    
class LtlList(list):

    def check_consistency(self, constraint, ltl_list, sigma):
        unpacked = sigma.top()
        for c in ltl_list:
            unpacked = unpacked & c
        
        slv = solver()
        xi = scope(sigma)

        f = unpacked & constraint # test consistency by testing the conjunction

        return slv.solve(xi,f,True)
    
    def check_redundancy(self, constraint, ltl_list, sigma):
        unpacked = sigma.top()
        for c in ltl_list:
            unpacked = unpacked & c
        
        slv = solver()
        xi = scope(sigma)

        f = implies(unpacked,constraint) # test redundancy by testing implication

        return slv.solve(xi,~f,True)
    
# test 
# constraint_list = [ChainResponse("a","b"), Succession("a","c"), Init("b"), AlternatePrecedence("b","d")]

# output_constraints = ""
# output1 = ""
# output2 = ""

# for item in constraint_list[:-1]:
#     item_str = str(item) + " | | |\n"
#     output1 += item_str

# for item in constraint_list[:-1]:
#     item_str = str(item) + " | | |\n"
#     item_str = item_str.replace("(","[")
#     item_str = item_str.replace(")","]")
#     item_str = item_str.replace(",",", ")
#     item_split = re.findall('[A-Z][^A-Z]*', item_str)
#     item_str = " ".join(str(item) for item in item_split)
#     output1 += item_str

# item_last_str = str(constraint_list[len(constraint_list)-1]) + " | |"
# item_last_str = item_last_str.replace("(","[")
# item_last_str = item_last_str.replace(")","]")
# item_last_str = item_last_str.replace(",",", ")
# item_split = re.findall('[A-Z][^A-Z]*', item_last_str)
# item_last_str = " ".join(str(item) for item in item_split)
# output2 = item_last_str

# output_constraints = output1 + output2
    
# Needed output

# activity activityname _newline activity activityname _newline ...
    # e.g. 
    # activity Create PR
    # activity Approve PR
# template (with spaces) [antecedent, consequent] | | | _newline ...
    # Chain Response[a, b] | | |
    # Chain Response[c, d] | | |
# last constraint: | | (to end)
    # Response[b, c] | | 


