from Constraint import *
from black_sat import *
# import time


class LtlList(list):

    def add_first_ltl(self,activities,sigma): 
        f = sigma.top()

        for a in activities: 
            activities_except_a = [x for x in activities if x != a]
            a = sigma.proposition(a)

            for b in activities_except_a:
                b = sigma.proposition(b)
                f = f & implies(a,~b)    

        return G(f)        

    def check_consistency(self, constraint, ltl_list, sigma):
        unpacked = sigma.top()
        for c in ltl_list:
            unpacked = unpacked & c
        
        slv = solver()
        xi = scope(sigma)

        f = unpacked & constraint # test consistency by testing the conjunction
        
        # st = time.time()
        print("consistency check...")

        n = 0
        result = slv.solve(xi,f,True,10)
        while (result == None): 
            n+=1
            result = slv.solve(xi,f,True,10)
            if result != None:
                return result
            elif n > 10: 
                return None
            else: continue

        # et = time.time()
        print("end consistency check")

        # elapsed_time_sec = et - st
        # print('Execution time:', elapsed_time_sec, 'seconds')
        
        return result

    def check_redundancy(self, constraint, ltl_list, sigma):
        unpacked = sigma.top()
        for c in ltl_list:
            unpacked = unpacked & c
        
        slv = solver()
        xi = scope(sigma)

        f = implies(unpacked,constraint) # test redundancy by testing the negation of the implication

        # st = time.time()
        print("redundancy check...")
            
        n = 0
        result = slv.solve(xi,~f,True,10)
        while (result == None): 
            n+=1
            result = slv.solve(xi,~f,True,10)
            if result != None:
                return result
            elif n > 10: 
                return None
            else: continue

        # et = time.time()
        print("end redundancy check")

        # elapsed_time_sec = et - st
        # print('Execution time:', elapsed_time_sec, 'seconds')

        return result
    
