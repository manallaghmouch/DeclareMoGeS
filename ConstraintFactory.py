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

    inconsistent_constraint = 0
    redundant_constraint = 0
    
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
    def create_consistent_model(self, alphabet_size, set_size, weights, consequent_not_adding, templates):
        constraint = Constraint()
        constraint_list = ConstraintList()
        ltl_list = LtlList()
        alphabet = Alphabet(alphabet_size)
        t = Templates(templates)
        initial_templates = templates

        ltl_list.append(ltl_list.add_first_ltl(alphabet.alphabet,self.sigma))
        # print([str(x) for x in ltl_list])

        self.inconsistent_constraint = 0
        self.redundant_constraint = 0
        n = 0 # number of times that a constraint was consequently not added to the model
        j = 0
        while j < set_size:
            if templates != []:
                potential_constraint = self.create_one_constraint_alphabet(t.templates, weights, alphabet)
                print("potential_constraint created: " + str(potential_constraint))
                # print([str(ltl_constraint)])
                if potential_constraint != None: 
                    ltl_constraint = constraint.declare_to_ltl(potential_constraint, self.sigma)
                    # consistency = ltl_list.check_consistency_timeout(ltl_constraint, ltl_list, self.sigma)
                    # redundancy = ltl_list.check_redundancy_timeout(ltl_constraint, ltl_list, self.sigma)   

                    consistency = ltl_list.check_consistency(ltl_constraint, ltl_list, self.sigma)
                    redundancy = ltl_list.check_redundancy(ltl_constraint, ltl_list, self.sigma)   

                    # consistency = self.do_or_stop_consistency_check(ltl_list,ltl_constraint,self.sigma)  
                    # redundancy = self.do_or_stop_redundancy_check(ltl_list,ltl_constraint,self.sigma)                                    
                    if (consistency == True and redundancy == True):
                        constraint_list.append(potential_constraint)
                        print(constraint_list)
                        ltl_list.append(ltl_constraint)
                        # print([str(x) for x in ltl_list])

                        deleted_template = t.change_templates(potential_constraint, alphabet)

                        if deleted_template != None:
                            t.delete_template_weight(deleted_template,initial_templates,weights)

                        n = 0
                        j += 1
                        # print("redundant_constraints: " + str(self.redundant_constraint) + "\ninconsistent_constraints: " + str(self.inconsistent_constraint))
                    elif consistency == False:
                        n += 1
                        self.inconsistent_constraint +=1
                        if n >= consequent_not_adding:  # after 5 subsequent constraints that could not be added to the model, we end the model creation
                            # current_set_size = len(constraint_list)
                            self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                            self.get_inconsistency()
                            self.get_redundancy()  
                            print(constraint_list)                          
                            return constraint_list
                        else: continue 
                    elif redundancy == False:
                        n += 1
                        self.redundant_constraint +=1
                        if n >= consequent_not_adding:  # after 5 subsequent constraints that could not be added to the model, we end the model creation
                            # current_set_size = len(constraint_list)
                            self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                            self.get_inconsistency()
                            self.get_redundancy()
                            print(constraint_list)
                            return constraint_list
                        else: continue 
                    else:
                        continue
                else:
                    n += 1 
                    if n >= consequent_not_adding: 
                        # current_set_size = len(constraint_list)
                        self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                        self.get_inconsistency()
                        self.get_redundancy()     
                        print(constraint)                   
                        return constraint_list
                    else: continue
            else:
                self.end_model_message("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.") 
                self.get_inconsistency()
                self.get_redundancy()   
                print(constraint_list)             
                return constraint_list
        self.get_inconsistency()
        self.get_redundancy()
        print(constraint_list)
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

    def get_inconsistency(self):
        print("inconsistent_constraints: " + str(self.inconsistent_constraint))
        return self.inconsistent_constraint

    def get_redundancy(self):
        print("redundant_constraints: " + str(self.redundant_constraint))
        return self.redundant_constraint

    # def do_or_stop_consistency_check(self,ltl_list,ltl_constraint,sigma):
    #     process = multiprocessing.Process(target=ltl_list.check_consistency(ltl_constraint, ltl_list, sigma))
    #     process.start()
    #     process.join(timeout=60)
    #     process.terminate()

    #     if process.exitcode is None:
    #         print('Timeout!')

    # def do_or_stop_redundancy_check(self,ltl_constraint,ltl_list,sigma):
    #     process = multiprocessing.Process(target=ltl_list.check_redundancy(ltl_constraint, ltl_list, sigma))
    #     process.start()
    #     process.join(timeout=60)
    #     process.terminate()

    #     if process.exitcode is None:
    #         print('Timeout!')


