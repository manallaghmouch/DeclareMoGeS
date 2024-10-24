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

    def specialise_model(self, initial_model, specialization_percentage, subset_to_keep): 
        constraint = Constraint()
        ltl_list = LtlList()
        hierarchy = Hierarchy()

        constraints_fixed = subset_to_keep 

        # Add constraints that cannot be specialized to the fixed list
        for c in initial_model:
            if not hierarchy.can_be_specialised(c): 
                constraints_fixed.append(c)

        constraints_to_specialize = [c for c in initial_model if c not in constraints_fixed]
        temp_model = ConstraintList(initial_model)

        self.inconsistent_constraint = 0
        self.redundant_constraint = 0
        self.time_exceeded = 0 
        self.model_differs = 0 

        stop_after = 10
        n = 0  # Unsuccessful attempts counter
        self.iterations = [] 
        j = 0

        if len(initial_model) == 0: 
            print("No specialization of initial model could be generated, because initial model is empty.")
            return temp_model  # Return the empty model

        for c in constraints_to_specialize:
            initial_constraint = c
            temp_model.remove(initial_constraint)
            temp_model_ltl = self.model_to_ltl(temp_model)
            
            # Check if the constraint can be specialized
            if hierarchy.can_be_specialised(initial_constraint):
                if random.random() < specialization_percentage:
                    potential_constraint = hierarchy.generate_specialisation_candidate(initial_constraint)
                    ltl_constraint = self.constraint.declare_to_ltl(potential_constraint, self.sigma)
                    
                    # Check the new constraint for consistency
                    consistency = ltl_list.check_consistency(ltl_constraint, temp_model_ltl, self.sigma, time_out=30)

                    if consistency: 
                        temp_model.append(potential_constraint)
                        self.iterations.append(n+1)
                        n = 0  # Reset unsuccessful attempts
                    else: 
                        temp_model.append(initial_constraint)
                        self.iterations.append(n+1)
                        n += 1

                    # Stop after too many unsuccessful attempts
                    if n >= stop_after: 
                        self.iterations.append(n+1)
                        self.model_differs = 1                         
                        return temp_model
                else: 
                    temp_model.append(initial_constraint)
            else:
                # If specialization is not possible, keep the original constraint
                temp_model.append(initial_constraint)

        return temp_model

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


