from Model import *
import pandas as pd
import time
import csv   

result1 = {
    "run": [],
    "scenario": [],
    "set_size_given": [],
    "set_size_actual": [],
    "alphabet_size": [],
    "stop_after": [],
    "inconsistencies": [],
    "redundancies": [],
    "exec_time_sec": [],
}
df3 = pd.DataFrame(result1)
df3.to_csv("result1-20.csv", sep=',')

result2 = {
    "run": [],
    "set_size": [],
    "alphabet_size": [],
    "end_model": []
}
df4 = pd.DataFrame(result2)
df4.to_csv("result2-20.csv", sep=',')

# baseline parameters
stop_after = 20 # constraints
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

i = 0
for set_size in range(20,51):
    for alphabet_size in range(5,31):
        for j in range(1):

            # start time
            st = time.time()

            # main program
            try: 
                model = Model("model6.decl", alphabet_size, set_size, weights, stop_after, templates)
            
                # end time
                et = time.time()

                # get the execution time
                elapsed_time_sec = et - st
                print('Execution time model:', elapsed_time_sec, 'seconds')

                res = et - st
                final_res = res * 1000
                # print('Execution time:', final_res, 'milliseconds')
                
                fields1 = [i, 
                            str(set_size) + " - " + str(alphabet_size), 
                            set_size, 
                            model.__len__(), 
                            alphabet_size, 
                            stop_after, 
                            model.get_inconsistency(), 
                            model.get_redundancy(), 
                            elapsed_time_sec]
                
                with open(r'result1-20.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields1)
                
                fields2 = [i, 
                            set_size, 
                            alphabet_size, 
                            str(model.constraint_list)]
                
                with open(r'result2-20.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields2)
            
            except Exception as err:
                # end time
                with open("error.txt", 'a') as file:
                    f.write(str(err))

            i += 1