from SpecializedModel import *
import pandas as pd
import time
import csv 
from sys import argv
import re

# df = pd.read_csv("G:/Shared drives/PhD Manal/Collaborations/Bozen-Bolzano/results_journal/specialized_models.csv", delimiter=";")
df = pd.read_csv(argv[2], delimiter=";")

def Convert_to_lst(str_lst): 
    str_lst = str_lst.replace("[", "")
    str_lst = str_lst.replace("]", "")
    li = list(str_lst.split(", ")) 
    return li 

# Define a dictionary to map class names to their corresponding classes
class_map = {
    'Choice': Choice,
    'ExclusiveChoice': ExclusiveChoice,
    'End': End,
    'Init': Init,
    'Existence': Existence,
    'Exactly': Exactly,
    'RespondedExistence': RespondedExistence,
    'CoExistence': CoExistence,
    'Response': Response,
    'Precedence': Precedence,
    'Succession': Succession,
    'AlternateResponse': AlternateResponse,
    'AlternatePrecedence': AlternatePrecedence,
    'AlternateSuccession': AlternateSuccession,
    'ChainResponse': ChainResponse,
    'ChainPrecedence': ChainPrecedence,
    'ChainSuccession': ChainSuccession,
    'NotCoExistence': NotCoExistence,
    'NotSuccession': NotSuccession,
    'NotChainSuccession': NotChainSuccession,
    'Absence': Absence
}

# Function to transform string into Constraint instance
def transform_item(item):
    # match = re.match(r'(\w+)\((\w+)(?:,(\w+))?\)', item)
    match = re.match(r'(\w+)\(([^,]+)(?:,(.+))?\)', item)
    if match:
        class_name = match.group(1)
        args = [match.group(2)]
        if match.group(3):
            args.append(match.group(3))
        if class_name in class_map:
            cls = class_map[class_name]
            return cls(*args)
    return item

# lst = ['ChainPrecedence(a,})', 'End(q)', 'NotChainSuccession(a,m)', 'ChainPrecedence(c,i)', 'NotChainSuccession(c,n)', 'Exactly(g)', 'ChainPrecedence(j,d)', 'ExclusiveChoice(l,q)', 'ChainPrecedence(b,h)', 'NotChainSuccession(j,c)', 'Exactly(b)']

# transformed_lst = [transform_item(item) for item in lst]

# for item in transformed_lst:
#     print(item)
df['generated_model'] = df['generated_model'].apply(lambda x: Convert_to_lst(x))
df['generated_model'] = df['generated_model'].apply(lambda x: [transform_item(item) for item in x])

# using iteritems() function to retrieve rows
for key, value in df.iterrows():
    print(key)
    print()

result2 = {
    "set_size_initial": [],
    "set_size_specialized": [],
    "specialization_percentage": [],
    "specialized_model": []
}
df_result = pd.DataFrame(result2)
df_result.to_csv("specialized_model{0}.csv".format(argv[1]), sep=',',index=False)

for series_name, series in df.generated_model.items():
    filename='specialisation.decl'
    initial_model = series
    percentage = random.random()

    st = time.time()
    specialized = SpecializedModel(filename,initial_model, percentage)
    et = time.time()

    exec_time = et - st

    fields2 = [len(initial_model),  
               len(specialized),
               percentage,
               specialized.constraint_list]

    with open(r"specialized_model{0}.csv".format(argv[1]), 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields2)















filename='hallo.decl'                            
initial_model = [Response('A','B'), Precedence('C','D')] 
specialisation = SpecializedModel(filename,initial_model)





# KLAD 
st_s70 = time.time()
specialized70 = SpecializedModel(filename,initial_model, 0.7)
et_s70 = time.time()

st_s50 = time.time()
specialized50 = SpecializedModel(filename,initial_model, 0.5)
et_s50 = time.time()

st_s30 = time.time()
specialized30 = SpecializedModel(filename,initial_model, 0.3)
et_s30 = time.time()