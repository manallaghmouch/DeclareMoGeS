from Constraint import *
from Templates import *
from Alphabet import *
from ConstraintList import *
from LtlList import *
from ConstraintFactory import *
from Hierarchy import *
from Model import *
import random
from black_sat import *

class SpecializedModel: 
    constraint = Constraint()
    constraintlist = ConstraintList()
    sigma = alphabet() # needed for satisfyability and redundancy checks with black_sat

    inconsistent_constraint = 0
    redundant_constraint = 0
    time_exceeded = 0
    model_differs = 0

    def __init__(self, filename, initial_model, specialization_percentage = 1, subset_to_keep = []):
        initial_model = ConstraintList(initial_model)
        self.constraint_list = self.specialise_model(initial_model, specialization_percentage, subset_to_keep)
        
        self.ltl_list = self.model_to_ltl(self.constraint_list)
        self.ltl_list_str = self.model_to_ltl_str()
        self.file = self.save_model(self.constraint_list, filename) 

    def specialise_model(self, initial_model, specialization_percentage, subset_to_keep): # user can indicate to keep a part of the initial model in the specialized model
        # to empty list if you already specialized once 
        constraint = Constraint()
        ltl_list = LtlList()
        hierarchy = Hierarchy()

        ## different lists of constraints
        # constraints_fixed = subset_to_keep + [x for x in initial_model if not x in subset_to_keep or if not x in ]

        constraints_fixed = subset_to_keep 

        for c in initial_model:
            if hierarchy.generate_specialisation_candidate(c) == False: 
                constraints_fixed.append(c)
            else: pass 

        constraints_to_specialize = [c for c in initial_model if not c in constraints_fixed]

        temp_model = ConstraintList(initial_model)

        ## Copy initial_model to temp_model (which we will change later on)
        # temp_model = [x for x in initial_model if not x in subset_to_keep or subset_to_keep.remove(x)]

        ## Check which rules from temp_model cannot be specialized
        # specialized_model_declare = constraints_fixed

        # for r in temp_model: 
        #     if hierarchy.can_be_specialised(r) == False: 
        #         specialized_model_declare.append(r)
        #         temp_model.remove(r)
        #     else:
        #         pass 

        ## Transform subset_to_keep to LTL list
        # specialized_model = self.model_to_ltl(specialized_model_declare) 

        # if subset_to_keep == []:
        #     specialized_model = []
        # else: specialized_model = specialized_model

        self.inconsistent_constraint = 0
        self.redundant_constraint = 0
        self.time_exceeded = 0 
        self.model_differs = 0 # salver took longer than 1 minute 

        stop_after = 10

        n = 0 # number of times that a constraint was consequently not added to the model
        self.iterations = [] # to save how many iterations were needed before adding a constraint to the model 
        j = 0

        if len(initial_model) == 0: 
            return print("No specialization of initial model could be generated, because initial model is empty.")
        else:
            for c in constraints_to_specialize:
                initial_constraint = c
                temp_model.remove(initial_constraint)
                temp_model_ltl = self.model_to_ltl(temp_model)
                
                if hierarchy.can_be_specialised(initial_constraint):
                    if random.random() < specialization_percentage:
                        # 1) specialiseren
                        potential_constraint = hierarchy.generate_specialisation_candidate(initial_constraint)
                        ltl_constraint = self.constraint.declare_to_ltl(potential_constraint, self.sigma)
                        
                        # 2) checks tov temp_model (model bevat de huidige constraint niet)
                        consistency = ltl_list.check_consistency(ltl_constraint, temp_model_ltl, self.sigma, time_out=30)
                        # inredundancy = ltl_list.check_redundancy(ltl_constraint, temp_model_ltl, self.sigma, time_out=30) 

                        # 3) na de checks: 
                        # 3.1) indien in orde - gespecialiseerde constraint toevoegen aan temp_model 
                        if consistency == True: 
                            temp_model.append(potential_constraint)
                            self.iterations.append(n+1)
                            n = 0
                            j += 1
                        # 3.2) indien niet in orde: niet-gespecialiseerde constraint terug toevoegen aan temp model OF opnieuw proberen te specialiseren             
                        else: 
                            temp_model.append(initial_constraint)
                            self.iterations.append(n+1)
                            n += 1

                            if n >= stop_after: 
                                # print("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
                                # self.get_inconsistency()
                                # self.get_redundancy()  
                                # print(constraint_list) 
                                self.iterations.append(n+1)
                                self.model_differs = 1                         
                                return temp_model
                            else: continue
        return temp_model
                     


        ## hierarchy = Hierarchy()
        ## n_initial_model = len(initial_model)
        n_initial_model = len(temp_model)

        # if n_initial_model == 0: 
        #     return print("No specialization of initial model could be generated, because initial model is empty.")
        # else:
        #     index = 0
        #     while index != n_initial_model:
        #         initial_constraint = initial_model[index]
        #         specialized_model_ltl = self.model_to_ltl(specialized_model)
        #         # hierarchy = Hierarchy()

        #         if hierarchy.can_be_specialised(initial_constraint):
        #             if random.random() < specialization_percentage:
        #                 potential_constraint = hierarchy.generate_specialisation_candidate(initial_constraint)
        #                 ltl_constraint = self.constraint.declare_to_ltl(potential_constraint, self.sigma)
        #                 consistency = ltl_list.check_consistency(ltl_constraint, specialized_model_ltl, self.sigma, time_out=30)
        #                 inredundancy = ltl_list.check_redundancy(ltl_constraint, specialized_model_ltl, self.sigma, time_out=30)

        #                 if (consistency == True and inredundancy == True):
        #                     ##
        #                     hierarchy = Hierarchy()
        #                     ##

        #                     specialized_model.append(potential_constraint)
        #                     ltl_list.append(ltl_constraint)
        #                     print("constraint added to specialized model")

        #                     self.iterations.append(n+1)
        #                     n = 0
        #                     j += 1

        #                     # to go further in the loop: 
        #                     index = index + 1

        #                 elif (consistency == False and inredundancy == False):
        #                     n += 1
        #                     self.inconsistent_constraint +=1
        #                     self.redundant_constraint +=1
        #                     print("Constraint not specialized. Let's try another specialisation candidate...")

        #                     hierarchy.delete_specialization_candidate(initial_constraint, potential_constraint)   

        #                     # to try again, and thus not go further in the loop: 
        #                     index = index    

        #                     if n >= stop_after: 
        #                         # print("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
        #                         # self.get_inconsistency()
        #                         # self.get_redundancy()  
        #                         # print(constraint_list) 
        #                         self.iterations.append(n+1)
        #                         self.model_differs = 1                         
        #                         return specialized_model
        #                     else: continue 

        #                 elif (consistency == True and inredundancy == False):
        #                     n += 1
        #                     self.redundant_constraint +=1
        #                     print("Constraint not specialized. Let's try another specialisation candidate...")

        #                     hierarchy.delete_specialization_candidate(initial_constraint, potential_constraint)   

        #                     # to try again, and thus not go further in the loop: 
        #                     index = index   

        #                     if n >= stop_after: 
        #                         # print("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
        #                         # self.get_inconsistency()
        #                         # self.get_redundancy()  
        #                         # print(constraint_list) 
        #                         self.iterations.append(n+1)
        #                         self.model_differs = 1                         
        #                         return specialized_model
        #                     else: continue 

        #                 elif (consistency == False and inredundancy == True):                                         
        #                     n += 1
        #                     self.inconsistent_constraint +=1
        #                     print("Constraint not specialized. Let's try another specialisation candidate...")

        #                     hierarchy.delete_specialization_candidate(initial_constraint, potential_constraint)   

        #                     # to try again, and thus not go further in the loop: 
        #                     index = index 

        #                     if n >= stop_after: 
        #                         # print("No model could be created given the current input parameters. To consult the last saved model check .constraint_list.")
        #                         # self.get_inconsistency()
        #                         # self.get_redundancy()  
        #                         # print(constraint_list) 
        #                         self.iterations.append(n+1)
        #                         self.model_differs = 1                         
        #                         return specialized_model
        #                     else: continue  

        #                 else: 
        #                     specialized_model.append(initial_constraint)
        #                     ltl_list.append(ltl_constraint)
        #                     n = 0

        # return specialized_model

    def has_specialisation_in_model(self, constraint, specialized_model): # In specialized model
        specialized_model_class = [specialized_constraint.__class__ for specialized_constraint in specialized_model]
        if constraint.__class__.__name__ == 'Precedence' or \
           constraint.__class__.__name__ == 'Response' or \
           constraint.__class__.__name__ == 'Succession' or \
           constraint.__class__.__name__ == 'AlternatePrecedence' or \
           constraint.__class__.__name__ == 'AlternateResponse' or \
           constraint.__class__.__name__ == 'AlternateSuccession' or \
           constraint.__class__.__name__ == 'ChainPrecedence' or \
           constraint.__class__.__name__ == 'ChainResponse' or \
           constraint.__class__.__name__ == 'RespondedExistence' or \
           constraint.__class__.__name__ == 'CoExistence' or \
           constraint.__class__.__name__ == 'NotSuccession' or \
           constraint.__class__.__name__ == 'NotChainSuccession' or \
           constraint.__class__.__name__ == 'Choice':

            candidate_list = Hierarchy.specialisation_candidates[constraint.__class__.__name__]

            potential_templates = list(set(candidate_list) & set(specialized_model_class))

            if potential_templates == []: 
                return False 
            else: 
                potential_constraints = []
                for i in range(len(potential_templates)): 
                    for j in range(len(specialized_model)):
                        if potential_templates[i] == specialized_model_class[j]:
                            potential_constraints.append(specialized_model[j])

                potential_constraints_str = [str(i) for i in potential_constraints]

                action = constraint.get_action()
                reaction = constraint.get_reaction()

                return any("{0},{1}".format(action,reaction) in i for i in potential_constraints_str)

        elif constraint.__class__.__name__ == 'Absence' or constraint.__class__.__name__ == 'Existence':
            return True 

        else: 
            return False 
    
    def model_to_ltl(self, constraint_list):
        constraint = Constraint()
        ltl_list = []
        for i in constraint_list:
            ltl_expression = constraint.declare_to_ltl(i, self.sigma)
            ltl_list.append(ltl_expression)
        return ltl_list
    
    def model_to_ltl_str(self):
        constraint = Constraint()
        ltl_list_str = []
        for i in self.constraint_list:
            ltl_expression = constraint.declare_to_ltl(i, self.sigma)
            ltl_list_str.append(str(ltl_expression))
        return ltl_list_str
    
    def get_inconsistency(self):
        return Model.cf.get_inconsistency()

    def get_redundancy(self):
        return Model.cf.get_redundancy()
    
    def get_time_exceeded(self):
        return Model.cf.get_time_exceeded()
    
    def get_model_differs(self):
        return Model.cf.get_model_differs()
    
    def get_iterations(self):
        return Model.cf.get_iterations_before_adding()

    def save_model(self, constraint_list, filename):
        file = open(filename, 'w',  encoding="utf-8") # overwrite if file already exists
        output = Model.constraintlist.list_to_decl_extension(constraint_list, activities=[])
        file.write(str(output))
        file.close()

    def check_model_consistency(self,specialized_model_declare):
        ltl_list = LtlList()
        specialized_model_ltl = self.model_to_ltl(specialized_model_declare)
        consistency = ltl_list.check_consistency_end_model(specialized_model_ltl, self.sigma, time_out=30)

        if consistency == True: 
            consistent_model = True 
        else: 
            consistent_model = False 
        
        return consistent_model     

    def check_model_inredundancy(self,specialized_model_declare):
        ltl_list = LtlList()
        specialized_model_ltl = self.model_to_ltl(specialized_model_declare)
        inredundancy = ltl_list.check_redundancy_end_model(specialized_model_ltl, self.sigma, time_out=30)

        if inredundancy == True: 
            inredundant_model = True 
        else: 
            inredundant_model = False 
        
        return inredundant_model     


