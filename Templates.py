from Constraint import *
from Alphabet  import *

class Templates:
    
    def __init__(self):
        self.templates = [Init, 
                          End, 
                          OneOrMore, 
                          OneAndOnlyOne, 
                          CoExistence, 
                          RespondedExistence, 
                          Response, 
                          Precedence, 
                          Succession, 
                          AlternateResponse, 
                          AlternatePrecedence, 
                          AlternateSuccession, 
                          ChainResponse, 
                          ChainPrecedence, 
                          ChainSuccession,
                          NotCoExistence, 
                          NotSuccession, 
                          NotChainSuccession,
                          Absence, 
                          Exactly,
                          Existence]
        
    def change_templates(self, constraint, alphabet):
        # get alphabets of constraint 
        if constraint.__class__.has_reaction():
            # check both the ante alpha and conse alpha
            constraint_actions = alphabet.alphabet_ante.get(constraint.__class__)
            constraint_reactions = alphabet.alphabet_conse.get(constraint.__class__)
            if ((len(constraint_actions) == 0) or (len(constraint_reactions) == 0)):
                # delete constraint template from templates
                self.templates.remove(constraint.__class__)
            else: pass 
        else: 
            constraint_actions = alphabet.alphabet_ante.get(constraint.__class__)
            if (len(constraint_actions) == 0):
                self.templates.remove(constraint.__class__)
            else: pass  