import random
from Constraint import *
from Alphabet import *
from ConstraintList import *
from Templates import *
from black_sat import *

# Random (not so random) constraint generator
class ConstraintFactory:
    """This class creates random constraints by combining a constraint template with activities"""
    sigma = alphabet()
    
    def __init__(self):
        pass
    
    def create_random(self, set_size, templates, weights, alphabet_size):
    # random_constraints = random.choice(templates)
        constraint_list = ConstraintList()

        alphabet = Alphabet(alphabet_size) 

        j=0
        while j < set_size:
            constraint = self.create_one_constraint_alphabet(templates, weights, alphabet)
            if not constraint_list.contains_constraint(constraint, constraint_list):
                constraint_list.append(constraint)
                j += 1
            else: continue 

        return constraint_list
    
    # added the consistency check below! 
    def create_consistent_model(self, alphabet_size, set_size, weights, templates):
        constraint = Constraint()
        constraint_list = ConstraintList()
        ltl_list = LtlList()

        template = Templates()
        alphabet = Alphabet(alphabet_size)

        n = 0 # number of times that a constraint was consequently not added to the model
        j = 0
        while j < set_size:
            potential_constraint = self.create_one_constraint_alphabet(templates, weights, alphabet)
            ltl_constraint = constraint.declare_to_ltl(potential_constraint, self.sigma)
            if ltl_constraint != None: 
                if (ltl_list.check_consistency(ltl_constraint, ltl_list, self.sigma) and ltl_list.check_redundancy(ltl_constraint, ltl_list, self.sigma)):
                    constraint_list.append(potential_constraint)
                    ltl_list.append(ltl_constraint)
                    template.change_templates(potential_constraint, alphabet)
                    n = 0
                    j += 1
                else: 
                    n += 1
                    if n >= 5:  # after 5 subsequent constraints that could not be added to the model, we end the model creation
                        # current_set_size = len(constraint_list)
                        self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                        return constraint_list
                    else: continue 
            else:
                n += 1 
                if n >= 5: 
                    # current_set_size = len(constraint_list)
                    self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                    return constraint_list
                else: continue
        return constraint_list

    def create_one_constraint_alphabet(self, templates, weights, alphabet, n=1):
        template_class = random.choices(templates, weights)[0]

        alpha_A = alphabet.alphabet_ante
        alpha_C = alphabet.alphabet_conse

        if template_class.has_reaction():
            if (len(alpha_A.get(template_class)) != 0 and len(alpha_C.get(template_class)) != 0): 
                constraint = template_class(action = random.choice(alpha_A.get(template_class)), reaction = random.choice(alpha_C.get(template_class)))
                alphabet.change_alphabet_A(constraint, alpha_A)
                alphabet.change_alphabet_C(constraint, alpha_C)
                return constraint
            else:
                constraint = None ##### AANPASSEN --> In dit geval is één van de alphabets leeg 
                return None

        elif template_class.has_n():
            constraint = template_class(action = random.choice(alpha_A.get(template_class)), n = random.randint(1,n)) # ik heb nu voor n gekozen van 1 tot 5
            alphabet.change_alphabet_A(constraint, alpha_A)
            alphabet.change_alphabet_C(constraint, alpha_C)
            return constraint

        else: 
            if len(alpha_A.get(template_class)) != 0:
                constraint = template_class(action = random.choice(alpha_A.get(template_class)))
                alphabet.change_alphabet_A(constraint, alpha_A)
                return constraint
            else: 
                return None   
            
    def end_model_message(self, message):
        # if after 10 potential constraints, none was added to the model
        # then: show message to user
        print(message)