# DeclareGeneratorSpecializer

## Installation 

STEP 1: Install BLACK (Bounded LTL Satisfiability Checker)

Installation guidelines are found on https://www.black-sat.org/en/stable/installation.html

STEP 2: Add BLACK to PATH

For Windows users: you need to add downloaded BLACK folder to PATH
For other users: follow the instructions on https://www.black-sat.org/en/stable/installation.html

STEP 3: Download this GitHub repository 


## Functions

### Model Generator

model_name = **Model**(filename,                            *string*
                    alphabet_size,                          *integer*
                    set_size,                               *integer*
                    weights,                                *list* - should be as long as list of templates
                    consequent_not_adding,                  *integer*
                    time_out,                               *integer* - in seconds
                    templates = [])                         *list* - if left empty, all templates are considered (21 templates in total)

*To show the model, you need to call (**constraint_list**)*

model_name.**constraint_list** 

### Model Specializer
 
model_name.**specialise_model**(specialization_percentage,  *float*
                                specialized_model = [])     *list*


## Some examples 

from Model import *

model1 = **Model**(filename="model1.decl",
               alphabet_size=10,
               set_size = 6,
               weights = [1,1,1,1,1],
               consequent_not_adding=10,
               time_out=60
               templates = [])

model1.constraint_list

model1.**specialise_model**(1)
model1.**specialise_model**(0.8)





 
