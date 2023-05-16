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
        'Absence': [Absence, Exactly],
        'Existence': [Existence, Exactly]
        #str(Absence(constraint.get_action, constraint.get_n)): []
        # Absence(n+1): [Absence(n), Exactly(n)],
        # Absence(n+2): [Absence(n), Absence(n+1), Exactly(n+1)],
        # Absence(n+K): [Absence(n-K), Absence(n-K+1), Exactly(n-K+1), Exactly(n)],
        # Exactly(n): [],
        # Exactly(n+1): []
        # Existence(n+1): [Exactly(n+1)]
        # Existence(n): [Exactly(n), Existence(n+1), Existence(n+2), ...]
        # RespondedExistence(b,a): [CoExistence, Precedence, AlternatePrecedence, ChainPrecedence, Succession, AlternateSuccession, CHainSuccession]
    }

    def __init__(self):
        pass

    def generate_specialisation_candidate(self, constraint):
        match constraint.__class__.__name__:
            case 'Precedence'|'Response'|'Succession'|'AlternatePrecedence'|'AlternateResponse'|'AlternateSuccession'|'ChainPrecedence'| \
                'ChainResponse'|'CoExistence'|'NotSuccession'|'NotChainSuccession'|'Choice':
                action = constraint.get_action()
                reaction = constraint.get_reaction()
                specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
                if specialized_template.has_reaction():
                    specialized_constraint = specialized_template(action, reaction)                
                else: 
                    specialized_constraint = specialized_template(action)    

            case 'RespondedExistence': # Een onderscheid gemaakt tussen de twee responded existences!!! (precedence vs. response)
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

            case 'Absence':
                action = constraint.get_action()
                n = constraint.get_n()
                specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
                if specialized_template == Absence:
                    specialized_constraint = random.choice([specialized_template(action,n),specialized_template(action,n - random.randint(1,n-1))])
                elif specialized_template == Exactly: 
                    if n>1: 
                        specialized_constraint = specialized_template(action, n-1) # instellen dat het nooit minder dan 1 mag zijn!
                    else:
                        pass # nog aanpassen -- nu slaat die dit geval over -- idealiter wil ik dat er dan opnieuw een specialisatie wordt gegenereerd

            case 'Existence':
                action = constraint.get_action()
                n = constraint.get_n()
                specialized_template = random.choice(Hierarchy.specialisation_candidates[constraint.__class__.__name__])
                if specialized_template == Exactly:
                    specialized_constraint = specialized_template(action,n)
                elif specialized_template == Existence: 
                    specialized_constraint = specialized_template(action,n + random.randint(1,4))

            case _: # Voor alle andere cases dupliceren we de constraint (vb. init)
                specialized_constraint = constraint                        

        return specialized_constraint

# Test
# hierarchy = Hierarchy()
# #model = [Response('a','b'), Precedence('c','d'), AlternatePrecedence('e','b'), RespondedExistence('k','i')]
# model1 = [RespondedExistence('k','i'), Precedence('a','b'), Init('b'), Init('a')] # We gaan er hier van uit dat de user een correct model meegeeft, want juiste 
# # activiteiten worden niet meer gecontroleerd
# hierarchy.specialise_model(model1)