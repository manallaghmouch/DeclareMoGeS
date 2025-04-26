from Model import * 

### Model Generation ###

templates = [
    RespondedExistence, Response, Precedence, AlternateResponse, 
    CoExistence, AlternatePrecedence, Succession, NotChainSuccession, 
    ChainResponse, ChainPrecedence, AlternateSuccession, Absence, 
    Existence, NotSuccession, ExclusiveChoice
]

template_weights = {template: random.uniform(0, 1) for template in templates}
weights_list = list(template_weights.values())

declare_model = Model(filename="declare_model_test.decl", 
                      alphabet_size=20,
                      set_size=10,
                      templates = templates,
                      weights = weights_list,
                      stop_after=10,
                      time_out=30
)

# Show constraints in declare_model
declare_model.constraint_list


### Model Specialization ###

specialized_declare_model = declare_model.specialise_model(filename="specialized_declare_model.decl", 
                                                           specialization_percentage=0.8,
                                                           specialized_model=[])

# Show constraints in specialized_declare_model
specialized_declare_model
