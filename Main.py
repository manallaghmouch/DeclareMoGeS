import numpy as np
import pandas as pd
from random import randrange
from Model import *
# import importlib
# importlib.reload(Model)
# from Model import *
import time

### Tests ###

### 1. Create random Declare model with all templates ###

# empty dataframe 

result1 = {
    "scenario": [],
    "run": [],
    "# constraints (asked)": [],
    "# constraint (actual)": [],
    "# activities": [],
    "conseq_not_adding_constraints": [],
    "# inconsistencies": [],
    "# redundancies": [],
    "execution time (seconds)": []
}

#load data into a DataFrame object:
df3 = pd.DataFrame(result1)

# baseline parameters
templates = [] # all templates
weights = [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1]

# Scenario 1
# stop_after = 20 # constraints
# i = 0
# for alphabet_size in range(5,20):
#     for set_size in range(5,20):
#         for j in range(50):

#             # start time
#             st = time.time()

#             # main program
#             model = Model("model6.decl", alphabet_size, set_size, weights, stop_after, templates)
#             model.constraint_list

#             # wait for 3 seconds
#             # time.sleep(3)
#             print(model.constraint_list)

#             # get the end time
#             et = time.time()

#             # get the execution time
#             elapsed_time_sec = et - st
#             print('Execution time:', elapsed_time_sec, 'seconds')

#             res = et - st
#             final_res = res * 1000
#             print('Execution time:', final_res, 'milliseconds')
        
#             df.loc[i] = [str(alphabet_size) + " - " + str(set_size), 
#                          str(i), 
#                          set_size, 
#                          model.__len__(), 
#                          alphabet_size, 
#                          stop_after, 
#                          model.get_inconsistency(), 
#                          model.get_redundancy(), 
#                          elapsed_time_sec]

#             i += 1


stop_after = 20 # constraints
i = 0
for alphabet_size in range(5,30):
    for set_size in range(5,50):
        for j in range(100):

            # start time
            st = time.time()

            # main program
            model = Model("model6.decl", alphabet_size, set_size, weights, stop_after, templates)
            model.constraint_list

            print(model.constraint_list)

            # end time
            et = time.time()

            # get the execution time
            elapsed_time_sec = et - st
            print('Execution time:', elapsed_time_sec, 'seconds')

            res = et - st
            final_res = res * 1000
            print('Execution time:', final_res, 'milliseconds')
            
            df3.loc[i] = [str(alphabet_size) + " - " + str(set_size), 
                        str(i), 
                        set_size, 
                        model.__len__(), 
                        alphabet_size, 
                        stop_after, 
                        model.get_inconsistency(), 
                        model.get_redundancy(), 
                        elapsed_time_sec]

            i += 1

print(df3)



