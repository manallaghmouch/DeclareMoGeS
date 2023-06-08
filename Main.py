from Model import *
import pandas as pd
import time
import csv 
from sys import argv

# set_size = argv[1]
# alphabet_size = argv[2]

# Files
time_file = time.time()

result1 = {
    "run": [],
    "scenario": [],
    "len_given": [],
    "len_actual": [],
    "alphabet_size": [],
    "stop_after": [],
    "inconsistencies": [],
    "redundancies": [],
    "exec_time_generator": [],
    "time_exceeded": [],
    "exec_time100": [],
    "exec_time70": [],
    "exec_time50": [],
    "exec_time30": []
}
df1 = pd.DataFrame(result1)
df1.to_csv("execution-{0}-{1}-{2}.csv".format(argv[1],argv[2],time_file), sep=',')

result2 = {
    "run": [],
    "set_size": [],
    "alphabet_size": [],
    "generated_model": [],
    "specialized100": [],
    "specialized70": [],
    "specialized50": [],
    "specialized30": [],
}
df2 = pd.DataFrame(result2)
df2.to_csv("model-{0}-{1}-{2}.csv".format(argv[1],argv[2],time_file), sep=',')

# Baseline parameters
stop_after = 20 # constraints
templates = [] # all templates
weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

# Main program
st_g = time.time()
model = Model("model6.decl", alphabet_size=argv[2], set_size=argv[1], weights=weights, stop_after=stop_after, templates=templates)
et_g = time.time()

# specialization scenarios
st_s100 = time.time()
specialized100 = model.specialise_model(1)
et_s100 = time.time() 

st_s70 = time.time()
specialized70 = model.specialise_model(0.7)
et_s70 = time.time() 

st_s50 = time.time()
specialized50 = model.specialise_model(0.5)
et_s50 = time.time() 

st_s30 = time.time()
specialized30 = model.specialise_model(0.3)
et_s30 = time.time() 

# get the execution time
exec_time_generator = et_g - st_g
exec_time100 = et_s100 - st_s100
exec_time70 = et_s70 - st_s70
exec_time50 = et_s50 - st_s50
exec_time30 = et_s30 - st_s30

# print('Execution time generator:', exec_time_generator, 'seconds')
# print('Execution time specializer:', exec_time_specializer, 'seconds')

fields1 = [str(argv[1]) + "-" + str(argv[2]), 
            argv[1], 
            model.__len__(), 
            argv[2], 
            stop_after, 
            model.get_inconsistency(), 
            model.get_redundancy(), 
            exec_time_generator,
            model.get_time_exceeded(),
            exec_time100,
            exec_time70,
            exec_time50,
            exec_time30
            ]

with open(r"model-{0}-{1}-{2}.csv".format(argv[1],argv[2],time_file), 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields1)

fields2 = [str(argv[1]) + "-" + str(argv[2]), 
            argv[1], 
            argv[2], 
            model.constraint_list,
            specialized100,
            specialized70,
            specialized50,
            specialized30]

with open("model-{0}-{1}-{2}.csv".format(argv[1],argv[2],time_file), 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields2)