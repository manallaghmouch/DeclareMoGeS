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

        keylist_ante = [Init, End, OneOrMore, OneAndOnlyOne, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, \
            AlternatePrecedence, AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

        keylist_conse = [CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, AlternatePrecedence, \
            AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

        self.alphabet_ante = {key: self.alphabet[:] for key in keylist_ante} 
        self.alphabet_conse = {key: self.alphabet[:] for key in keylist_conse}

        #Alphabet.alphabet_action = {key: alphabet for key in Alphabet.alphabet_action}
        #Alphabet.alphabet_reaction = {key: alphabet for key in Alphabet.alphabet_reaction}
  
    def change_alphabet_A(self, constraint, alphabet_A = alphabet_ante):
        match constraint.__class__.__name__:
            # niet nodig want wordt al uitgesloten door de dependencies
            # case 'Init':
            # case 'End':
            # templates that can only occur once with the same action -- delete action
            case 'OneOrMore':
                action = constraint.get_action()
                alphabet_A[OneOrMore].remove(str(action))
                return alphabet_A
            case 'OneAndOnlyOne':
                action = constraint.get_action()
                alphabet_A[OneAndOnlyOne].remove(str(action))
                return alphabet_A
            case 'AlternateResponse':
                action = constraint.get_action()
                alphabet_A[AlternateResponse].remove(str(action)) 
                # er gaat hier wat mis --> ALLE waardan voor de template worden verwijderdfrom Constraint import *
                # EN alle actions die overeenkomen worden in de andere lijsten verwijderd
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
            case 'ChainSuccession': # ook nog ander scenario toevoegen: chain succession(A,B) en succession(A,B) mogen niet samen voorkomen
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
            # niet nodig want wordt al uitgesloten door de dependencies
            # case 'Init':
            # case 'End':
            # templates that can only occur once with the same action -- delete action
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


# from Constraint import *

# class Alphabet:
#     alphabet_ante = None
#     alphabet_conse = None

#     def __init__(self, alphabet_size, alphabet = []):
#         alphabet = []
#         start = ord('a')
#         for i in range(alphabet_size):
#             alphabet.append(chr(start + i))

#         # list of constraints that can only occur once with the same antecedent
#         keylist_ante = [Init, End, OneOrMore, OneAndOnlyOne, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, \
#             AlternatePrecedence, AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

#         # list of constraints that can only occur once with the same consequent

    
#         keylist_conse = [CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, AlternatePrecedence, \
#             AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

#         Alphabet.alphabet_ante = {key: alphabet[:] for key in keylist_ante} 
#         Alphabet.alphabet_conse = {key: alphabet[:] for key in keylist_conse}

#     def change_alphabet_A(self, constraint, alphabet_A = alphabet_ante):
#         action = constraint.get_action()
#         if constraint.__class__.__name__ in alphabet_A:
#             alphabet_A[constraint.__class__.__name__].remove(str(action))
#         return alphabet_A

#     def change_alphabet_C(self, constraint, alphabet_C = alphabet_conse):
#         reaction = constraint.get_reaction()
#         if constraint.__class__.__name__ in alphabet_C:
#             alphabet_C[constraint.__class__.__name__].remove(str(reaction))
#         return alphabet_C


# class Alphabet:
#     alphabet_ante = None
#     alphabet_conse = None

#     def __init__(self, alphabet_size, alphabet = []):
#         alphabet = []
#         start = ord('a')
#         for i in range(alphabet_size):
#             alphabet.append(chr(start + i))

#         keylist_ante = [Init, End, OneOrMore, OneAndOnlyOne, CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, \
#             AlternatePrecedence, AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

#         keylist_conse = [CoExistence, RespondedExistence, Response, Precedence, Succession, AlternateResponse, AlternatePrecedence, \
#             AlternateSuccession, ChainResponse, ChainPrecedence, ChainSuccession, NotCoExistence, NotSuccession, NotChainSuccession]

#         Alphabet.alphabet_ante = {key: alphabet[:] for key in keylist_ante} 
#         Alphabet.alphabet_conse = {key: alphabet[:] for key in keylist_conse}

#     def change_alphabet_A(self, constraint, alphabet_A = alphabet_ante):
#         action = constraint.get_action()
#         if constraint.__class__.__name__ in alphabet_A:
#             alphabet_A[constraint.__class__.__name__].remove(str(action))
#         return alphabet_A

#     def change_alphabet_C(self, constraint, alphabet_C = alphabet_conse):
#         reaction = constraint.get_reaction()
#         if constraint.__class__.__name__ in alphabet_C:
#             alphabet_C[constraint.__class__.__name__].remove(str(reaction))
#         return alphabet_C