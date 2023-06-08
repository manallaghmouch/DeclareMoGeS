from Constraint import *
from ConstraintList import *
import random

class Hierarchy: 
    """This class defines hierarchies between Declare constraints in terms of specialisation"""

    # obv stronger-weaker relations Schunselaars: enkel met identiek dezelfde antecedent en consequent!
    specialisation_candidates = {
        'Precedence': [Init, AlternatePrecedence, ChainPrecedence, Succession, AlternateSuccession, ChainSuccession],
        'Response': [AlternateResponse, ChainResponse, Succession, AlternateSuccession, ChainSuccession],
        'Succession': [AlternateSuccession, ChainSuccession],
        'AlternatePrecedence': [AlternateSuccession, ChainSuccession, ChainPrecedence],
        'AlternateResponse': [AlternateSuccession, ChainSuccession, ChainResponse],
        'AlternateSuccession': [ChainSuccession],
        'ChainPrecedence': [ChainSuccession],
        'ChainResponse': [ChainSuccession],
        'RespondedExistence': [CoExistence, AlternateSuccession, ChainSuccession, Response, AlternateResponse, ChainResponse, Succession, Precedence, AlternatePrecedence, ChainPrecedence],
        'CoExistence': [Succession, AlternateSuccession, ChainSuccession],
        'NotSuccession': [NotCoExistence],
        'NotChainSuccession': [NotSuccession],
        'Choice': [ExclusiveChoice],
        # 'Absence': [Exactly], # Absence
        'Existence': [Exactly] # Existence
    }

    def __init__(self):
        pass

    def generate_specialisation_candidate(self, constraint):
        if constraint.__class__.__name__ == 'Precedence' or \
           constraint.__class__.__name__ == 'Response' or \
           constraint.__class__.__name__ == 'Succession' or \
           constraint.__class__.__name__ == 'AlternatePrecedence' or \
           constraint.__class__.__name__ == 'AlternateResponse' or \
           constraint.__class__.__name__ == 'AlternateSuccession' or \
           constraint.__class__.__name__ == 'ChainPrecedence' or \
           constraint.__class__.__name__ == 'ChainResponse' or \
           constraint.__class__.__name__ == 'CoExistence' or \
           constraint.__class__.__name__ == 'NotSuccession' or \
           constraint.__class__.__name__ == 'NotChainSuccession' or \
           constraint.__class__.__name__ == 'Choice':
            action = constraint.get_action()
            reaction = constraint.get_reaction()
            specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
            if specialized_template.has_reaction():
                specialized_constraint = specialized_template(action, reaction)                
            else: 
                specialized_constraint = specialized_template(action)    

        elif constraint.__class__.__name__ == 'RespondedExistence': # Een onderscheid gemaakt tussen de twee responded existences!!! (precedence vs. response)
            action = constraint.get_action()
            reaction = constraint.get_reaction()
            specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
            #specialized_constraint = specialized_template(action, reaction)
            if specialized_template == CoExistence | specialized_template == Succession | specialized_template == AlternateSuccession | \
                specialized_template == ChainSuccession:
                specialized_constraint = random.choice[specialized_template(action, reaction), specialized_template(reaction, action)]
            elif specialized_template == Response | specialized_template == AlternateResponse | specialized_template == ChainResponse:
                specialized_constraint = specialized_template(action, reaction) 
            else: 
                specialized_constraint = specialized_template(reaction, action)

        elif constraint.__class__.__name__ == 'Existence':
            action = constraint.get_action()
            # n = constraint.get_n()
            specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
            specialized_constraint = specialized_template(action)

        # case 'Absence':
        #     action = constraint.get_action()
        #     # n = constraint.get_n()
        #     specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
        #     if specialized_template == Absence:
        #         specialized_constraint = random.choice([specialized_template(action,n),specialized_template(action,n - random.randint(1,n-1))])
        #     elif specialized_template == Exactly: 
        #         if n>1: 
        #             specialized_constraint = specialized_template(action, n-1) # instellen dat het nooit minder dan 1 mag zijn!
        #         else:
        #             pass # nog aanpassen -- nu slaat die dit geval over -- idealiter wil ik dat er dan opnieuw een specialisatie wordt gegenereerd

        # case 'Existence':
        #     action = constraint.get_action()
        #     # n = constraint.get_n()
        #     specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
        #     if specialized_template == Exactly:
        #         specialized_constraint = specialized_template(action,n)
        #     elif specialized_template == Existence: 
        #         specialized_constraint = specialized_template(action,n + random.randint(1,4))

        else: # Voor alle andere cases nemen we dezelfde constraint over in het specialized_model (vb. init)
            specialized_constraint = False                  

        return specialized_constraint
    
    def can_be_specialised(self, constraint):
        if self.generate_specialisation_candidate(constraint) == False:
            return False
        else: return True 


# Test
# hierarchy = Hierarchy()
# #model = [Response('a','b'), Precedence('c','d'), AlternatePrecedence('e','b'), RespondedExistence('k','i')]
# model1 = [RespondedExistence('k','i'), Precedence('a','b'), Init('b'), Init('a')] # We gaan er hier van uit dat de user een correct model meegeeft, want juiste 
# # activiteiten worden niet meer gecontroleerd
# hierarchy.specialise_model(model1)