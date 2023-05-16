from Constraint import *
from Alphabet import *
from ConstraintList import *
from ConstraintFactory import *
from Hierarchy import *
import random
from black_sat import *

class Model: 
    cf = ConstraintFactory()
    constraint = Constraint()
    constraintlist = ConstraintList()
    sigma = alphabet()
    # alpha = Alphabet(alphabet_size)

    def __init__(self, alphabet_size, set_size, weights, templates, filename):
        # self.constraint_list = Model.cf.create_random(alphabet_size, set_size, weights, templates)
        self.constraint_list = Model.cf.create_consistent_model(alphabet_size, set_size, weights, templates)
        self.ltl_list = self.model_to_ltl()

        self.activities = Alphabet(alphabet_size).alphabet
        self.file = self.save_model(self.constraint_list, self.activities, filename)
        # self.activities = self.alpha.get_alphabet()
        # return model

    def __len__(self): # get the number of constraints in the generated model
        return len(self.constraint_list)

    def create_model(self, alphabet_size, set_size, weights, templates):
        model = Model.cf.create_consistent_model(alphabet_size, set_size, weights, templates)
        return model
    
    def model_to_ltl(self):
        constraint = Constraint()
        ltl_list = []
        for i in self.constraint_list:
            ltl_expression = constraint.declare_to_ltl(i, self.sigma)
            ltl_list.append(ltl_expression)
        return ltl_list

    def count_rules(self):
        pass 

    def specialise_model(self,specialized_model=[]): # user can indicate that he wants to keep a part of the initial model
        # Iterate over each constraint in the model
        hierarchy = Hierarchy()
        n_initial_model = self.__len__()

        # Add first specialized constraint to specialized model -- Indien er niet gespec kan worden, dan wordt de constraint overgenomen
        if n_initial_model == 0: 
            return cf.end_model_message("No specialization of initial model could be generated, because initial model is empty.")
        else:
            first_specialized_constraint = hierarchy.generate_specialisation_candidate(self.constraint_list[0])
            specialized_model.append(first_specialized_constraint)
            
            for index in range(1, n_initial_model):
                initial_constraint = self.constraint_list[index]
                if self.has_specialisation_in_model(initial_constraint, specialized_model):
                        random_choice = random.randint(0, 1) # Op dit moment 50% kans -- CHANGE: user input 
                        if random_choice==1:
                            specialized_constraint = hierarchy.generate_specialisation_candidate(initial_constraint)
                            
                            if not self.constraint_list.contains_constraint(specialized_constraint, specialized_model): # Indien template niet onderhevig aan dependency, 
                                # dan toevoegen
                                specialized_model.append(specialized_constraint)
                            else: 
                                pass
                        else: 
                            pass
                else:
                    specialized_constraint = hierarchy.generate_specialisation_candidate(initial_constraint)
                    if not self.constraint_list.contains_constraint(specialized_constraint, specialized_model): 
                        specialized_model.append(specialized_constraint)                
    
            return specialized_model

    def has_specialisation_in_model(self, constraint, specialized_model): # In specialized model
        match constraint.__class__.__name__:
            case 'Precedence'|'Response'|'Succession'|'AlternatePrecedence'|'AlternateResponse'|'AlternateSuccession'|'ChainPrecedence'| \
                'ChainResponse'|'RespondedExistence'|'CoExistence'|'NotSuccession'|'NotChainSuccession'|'Choice':
                candidate_list = Hierarchy.specialisation_candidates[constraint.__class__.__name__]

                specialized_model_class = [specialized_constraint.__class__ for specialized_constraint in specialized_model]
                return bool(set(candidate_list) & set(specialized_model_class))

                # for candidate_constraint in candidate_list:
                #     if candidate_constraint in specialized_model:
                #         return True
                #     else:

                #         return False 

            case 'Absence'|'Existence':
                return True 

            case _: return False 

    def check_consistency_model(self):
        slv = solver()
        xi = scope(self.sigma)

        unpacked = self.sigma.top()

        for c in self.ltl_list:
            unpacked = unpacked & c

        f = unpacked # test consistency by testing the conjunction

        return slv.solve(xi,f,True)
    
    def save_model(self, constraint_list, activities, filename):
        file = open(filename, 'w') # overwrites if file already exists
        output = Model.constraintlist.list_to_decl_extension(constraint_list, activities)
        file.write(str(output))
        file.close()
    
# Test

alphabet_size = 10 ### er gaat iets mis met de alphabet size 
set_size = 4
weights = [1]
templates = [RespondedExistence]

model = Model(3, set_size, weights, templates, "model6.decl")
model.constraint_list
model.specialise_model()
# model.model_to_ltl()




# TEST black 
# templates = [RespondedExistence]
# weights = [1]
# alphabet_size = 6
# set_size = 2

# sigma = alphabet()

# model = Model(alphabet_size, set_size, weights, templates)
# d = sigma.proposition('d')
# d = sigma.proposition('d')
# potential_constraint = implies(F(d), F(d))

# model.check_consistency_constraint(potential_constraint)

# # previous black test 
# model = Model(alphabet_size, set_size, templates, weights)
# model.constraint_list
# model.ltl_list

# sigma = alphabet()

# model_ltl = model.ltl_list 

# unpacked = sigma.top() # means True -- starting value 
# for c in model_ltl:
#     unpacked = unpacked & c

# d = sigma.proposition('d')
# d = sigma.proposition('d')
# potential_constraint = implies(F(d), F(d))

# slv = solver()
# xi = scope(sigma)

# f = unpacked & potential_constraint # test consistency by testing the conjunction
# f = implies(unpacked,potential_constraint) # test redundancy by testing implication

# slv.solve(xi,~f,True)

# Test
# set_size = 15
# alphabet_size = 5
# templates = [
#     Init, 
#     End, 
#     OneOrMore, 
#     OneAndOnlyOne, 
#     CoExistence, 
#     RespondedExistence, 
#     Response, 
#     Precedence, 
#     Succession, 
#     AlternateResponse, 
#     AlternatePrecedence, 
#     AlternateSuccession, 
#     ChainResponse, 
#     ChainPrecedence, 
#     ChainSuccession,
#     NotCoExistence, 
#     NotSuccession, 
#     NotChainSuccession,
#     Absence, 
#     Exactly,
#     Existence]
# # the probabilities are initial probabilities 
# weights = [
#     0.2,
#     0,
#     0,
#     0,
#     0.5,
#     0,
#     0,
#     0.1,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0.5,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0]

# model = Model(alphabet_size, set_size, templates, weights)
# print(model)

# model.specialise_model()

#specialisation_model = Model.specialise_model(model, model)

# model = Model()
# initial_model = model.create_model(set_size, templates, weights, alphabet_size)
# model.specialise_model(initial_model, 1)

