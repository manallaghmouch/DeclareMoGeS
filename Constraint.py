from black_sat import *

class Constraint:
    HAS_REACTION = False
    HAS_N = False

    sigma = alphabet()
    
    def check_constraint(self, constraint, eventlog):
        pass

    def get_action(self): 
        """
        This function takes a Declare Constraint as input and returns the antecedent of the constraint.
        """
        self.list_action_reaction = list(self.__dict__.items())
        self.action_value = self.list_action_reaction[0][1]
        return self.action_value
    
    def get_reaction(self):
        """
        This function takes a Declare Constraint as input and returns the consequent of the constraint.
        """ 
        self.list_action_reaction = list(self.__dict__.items())
        self.reaction_value = self.list_action_reaction[1][1]
        return self.reaction_value
    
    def get_n(self):
        self.list_n = list(self.__dict__.items())
        self.n_value = self.list_n[1][1]
        return self.n_value
    
    def declare_to_ltl(self, constraint, sigma):        
        if constraint.__class__.has_reaction():
            # action = constraint.get_action()
            # reaction = constraint.get_reaction()
            action = sigma.proposition(constraint.get_action())
            reaction = sigma.proposition(constraint.get_reaction())

            match constraint.__class__.__name__:
                case 'RespondedExistence':
                    return implies(F(action), F(reaction))
                case 'CoExistence':
                    return iff(F(action),F(reaction))
                case 'Response':
                    return G(implies(action,F(reaction)))
                case 'Precedence':
                    return U(~reaction,action) | G(~reaction)
                case 'Succession':
                    return G(implies(action,F(reaction))) & U(~reaction,action) | G(~reaction)
                case 'AlternateResponse':
                    return G(implies(action, X(U(~action,reaction))))
                case 'AlternatePrecedence': 
                    return (U(~reaction,action) | G(~reaction)) & G(implies(reaction, X((U(~reaction,action) | G(~reaction)))))
                case 'AlternateSuccession':
                    return G(implies(action, X(U(~action,reaction)))) & (U(~reaction,action) | G(~reaction)) & G(implies(reaction, X((U(~reaction,action) | G(~reaction)))))
                case 'ChainResponse':
                    return G(implies(action, X(reaction)))
                case 'ChainPrecedence':
                    return G(implies(X(reaction), action))
                case 'ChainSuccession':
                    return G(implies(action,X(reaction)) & G(implies(X(reaction),action)))
                case 'NotCoExistence':
                    return ~(iff(F(action),F(reaction)))
                case 'NotSuccession':
                    return ~(G(implies(action,F(reaction))) & U(~reaction,action) | G(~reaction))
                case 'NotChainSuccession':
                    return ~(G(implies(action,X(reaction)) & G(implies(X(reaction),action))))
                case 'Choice':
                    return F(action) | F(reaction)
                case 'ExclusiveChoice':
                    return (F(action) | F(reaction)) & ~(F(action) & F(reaction))
                case _: return None 
        
        elif not constraint.__class__.has_reaction():
            action = sigma.proposition(constraint.get_action())
            match constraint.__class__.__name__:
                case 'End': 
                    return F(~X(self.sigma.top()) & action)
                case 'Init':
                    return action
                case 'Absence': 
                    return ~(F(action))
                case 'Exactly': 
                    return F(action & X(~F(action))) 
                case 'Existence': 
                    return F(action)
                case _: return None
        
        else: return None 
                
    @classmethod
    def has_reaction(cls):
        return cls.HAS_REACTION
    
    @classmethod
    def has_n(cls):
        return cls.HAS_N
    

# Define constraint templates
class Choice(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"Choice({self.action},{self.reaction})"
    def __str__(self):
        return f"Choice({self.action},{self.reaction})"
    
class ExclusiveChoice(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"ExclusiveChoice({self.action},{self.reaction})"
    def __str__(self):
        return f"ExclusiveChoice({self.action},{self.reaction})"

class End(Constraint):
    HAS_REACTION = False
    HAS_N = False
    action = None
    #dependency = [MaxOne]
    def __init__(self, action):
        self.action = action
    def __repr__(self):
        return f"End({self.action})"
    def __str__(self):
        return f"End({self.action})"

class Init(Constraint):
    HAS_REACTION = False
    HAS_N = False
    action = None
    def __init__(self, action):
        self.action = action
    def __repr__(self):
        return f"Init({self.action})"
    def __str__(self):
        return f"Init({self.action})"

class Existence(Constraint):
    HAS_REACTION = False
    HAS_N = False
    action = None
    def __init__(self, action):
        self.action = action
    def __repr__(self):
        return f"Existence({self.action})"
    def __str__(self):
        return f"Existence({self.action})"

class Exactly(Constraint):
    HAS_REACTION = False
    HAS_N = False
    action = None
    def __init__(self, action):
        self.action = action
    def __repr__(self):
        return f"Exactly({self.action})"
    def __str__(self):
        return f"Exactly({self.action})" 

class RespondedExistence(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"RespondedExistence({self.action},{self.reaction})"
    def __str__(self):
        return f"RespondedExistence({self.action},{self.reaction})"

class CoExistence(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action =  None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"CoExistence({self.action},{self.reaction})"
    def __str__(self):
        return f"CoExistence({self.action},{self.reaction})" 

class Response(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"Response({self.action},{self.reaction})"
    def __str__(self):
        return f"Response({self.action},{self.reaction})"

class Precedence(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"Precedence({self.action},{self.reaction})"
    def __str__(self):
        return f"Precedence({self.action},{self.reaction})"

class Succession(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"Succession({self.action},{self.reaction})"
    def __str__(self):
        return f"Succession({self.action},{self.reaction})"

class AlternateResponse(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"AlternateResponse({self.action},{self.reaction})"
    def __str__(self):
        return f"AlternateResponse({self.action},{self.reaction})"

class AlternatePrecedence(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"AlternatePrecedence({self.action},{self.reaction})"
    def __str__(self):
        return f"AlternatePrecedence({self.action},{self.reaction})"

class AlternateSuccession(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"AlternateSuccession({self.action},{self.reaction})"
    def __str__(self):
        return f"AlternateSuccession({self.action},{self.reaction})"

class ChainResponse(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"ChainResponse({self.action},{self.reaction})"
    def __str__(self):
        return f"ChainResponse({self.action},{self.reaction})"

class ChainPrecedence(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"ChainPrecedence({self.action},{self.reaction})"
    def __str__(self):
        return f"ChainPrecedence({self.action},{self.reaction})"

class ChainSuccession(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"ChainSuccession({self.action},{self.reaction})"
    def __str__(self):
        return f"ChainSuccession({self.action},{self.reaction})"

class NotCoExistence(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"NotCoExistence({self.action},{self.reaction})"
    def __str__(self):
        return f"NotCoExistence({self.action},{self.reaction})"

class NotSuccession(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"NotSuccession({self.action},{self.reaction})"
    def __str__(self):
        return f"NotSuccession({self.action},{self.reaction})"

class NotChainSuccession(Constraint):
    HAS_REACTION = True
    HAS_N = False
    action = None
    reaction = None
    def __init__(self, action, reaction):
        self.action = action
        self.reaction = reaction
    def check(self): 
        pass
    def __repr__(self):
        return f"NotChainSuccession({self.action},{self.reaction})"
    def __str__(self):
        return f"NotChainSuccession({self.action},{self.reaction})"

class Absence(Constraint):
    HAS_REACTION = False
    HAS_N = True 
    action = None
    reaction = None
    n = None
    def __init__(self, action):
        self.action = action
        # self.n = n 
    def check(self): 
        pass
    def __repr__(self):
        return f"Absence({self.action})"
    def __str__(self):
        return f"Absence({self.action})"