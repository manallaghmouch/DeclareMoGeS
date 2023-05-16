import numpy as np
import pandas as pd
from random import randrange
from Model import *
from log_deviations import *

# OK! Alphabet_size toevoegen: zie model.py
# +/- Dependencies regels implementeren: zie constraint_factory.py, dependency.py
# Distributie toevoegen: definieer een verdeling vb. 50% kans op X regels, 20% kans op X regels, ...
# Step 2: specialize model (obv theorema)

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


