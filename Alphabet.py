from Constraint import *

class Alphabet:
    alphabet_ante = None
    alphabet_conse = None
    alphabet = []

    def __init__(self, alphabet_size):
        self.alphabet = []
        start = ord('a')
        for i in range(alphabet_size):
            self.alphabet.append(chr(start + i))

        keylist_ante = [Choice, ExclusiveChoice, Init, End, Absence, Existence, Exactly, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, \
            AlternatePrecedence, AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

        keylist_conse = [Choice, ExclusiveChoice, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, AlternatePrecedence, \
            AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

        self.alphabet_ante = {key: self.alphabet[:] for key in keylist_ante} 
        self.alphabet_conse = {key: self.alphabet[:] for key in keylist_conse}
  
    def change_alphabet_A(self, constraint, alphabet_A = alphabet_ante):
        match constraint.__class__.__name__:
            # templates that can only occur once with the same action -- delete action
            case 'Existence':
                action = constraint.get_action()
                alphabet_A[Existence].remove(str(action))
                return alphabet_A
            case 'Exactly':
                action = constraint.get_action()
                alphabet_A[Exactly].remove(str(action))
                return alphabet_A
            case 'AlternateResponse':
                action = constraint.get_action()
                alphabet_A[AlternateResponse].remove(str(action)) 
                return alphabet_A
            case 'AlternatePrecedence':
                action = constraint.get_action()
                alphabet_A[AlternatePrecedence].remove(str(action))
                return alphabet_A
            case 'AlternateSuccession':
                action = constraint.get_action()
                alphabet_A[AlternateSuccession].remove(str(action))
                return alphabet_A
            case 'ChainResponse':
                action = constraint.get_action()
                alphabet_A[ChainResponse].remove(str(action))
                return alphabet_A.get(ChainResponse)
            case 'ChainPrecedence':
                action = constraint.get_action()
                alphabet_A[ChainPrecedence].remove(str(action))
                return alphabet_A
            case 'ChainSuccession': 
                action = constraint.get_action()
                alphabet_A[ChainSuccession].remove(str(action))
                return alphabet_A
            # templates that cannot occur together with the same action and reaction
            case 'CoExistence':
                # delete action and reaction
                action = constraint.get_action()
                alphabet_A[CoExistence].remove(str(action))
                return alphabet_A
            case 'NotCoExistence':
                action = constraint.get_action()
                alphabet_A[NotCoExistence].remove(str(action))
                return alphabet_A
            case 'Succession':
                action = constraint.get_action()
                alphabet_A[Succession].remove(str(action))
                return alphabet_A  
            case 'NotSuccession':
                action = constraint.get_action()
                alphabet_A[NotSuccession].remove(str(action))
                return alphabet_A
            case 'NotChainSuccession':
                action = constraint.get_action()
                alphabet_A[NotChainSuccession].remove(str(action))
                return alphabet_A                  
            case _: return alphabet_A

    def change_alphabet_C(self, constraint, alphabet_C = alphabet_conse):
        match constraint.__class__.__name__:
            # templates that cannot occur together with the same action and reaction
            case 'CoExistence':
                # delete action and reaction
                reaction = constraint.get_reaction()
                alphabet_C[CoExistence].remove(str(reaction))
                return alphabet_C
            case 'NotCoExistence':
                reaction = constraint.get_reaction()
                alphabet_C[NotCoExistence].remove(str(reaction))
                return alphabet_C
            case 'Succession':
                reaction = constraint.get_reaction()
                alphabet_C[Succession].remove(str(reaction))
                return alphabet_C 
            case 'NotSuccession':
                reaction = constraint.get_reaction()
                alphabet_C[NotSuccession].remove(str(reaction))
                return alphabet_C
            case 'NotChainSuccession':
                reaction = constraint.get_reaction()
                alphabet_C[NotChainSuccession].remove(str(reaction))
                return alphabet_C             
            case _: return alphabet_C