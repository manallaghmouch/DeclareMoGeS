import numpy as np
import pandas as pd
from random import randrange
from Model import *

# create normative model
Model1 = Model(alphabet_size=1, number_of_constraints=5)
Model1.create_model()
print(Model1.model)


Model2 = Model(alphabet_size=10, number_of_constraints=5)

# Test: Create an instance of ConstraintFactory and generate a random list of constraints given the number of constraints
cf = ConstraintFactory()
constraint_list = cf.create_random(5, [Response,Init], ["A", "B", "C", "D"])
print(constraint_list)

# Create a normative model that consists of a set of random constraints that use a given alphabet of activities
Model1.create_model()
model2 = Model2.create_model()
print(Model1.model)
print(model2)


# TESTS MODEL

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



