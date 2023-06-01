# from __future__ import print_function
from Constraint import *
from black_sat import *
import re
# import sys
# import threading
import multiprocessing
import time
# from time import sleep
# try:
#     import thread
# except ImportError:
#     import _thread as thread

# try:
#     range, _print = xrange, print
#     def print(*args, **kwargs): 
#         flush = kwargs.pop('flush', False)
#         _print(*args, **kwargs)
#         if flush:
#             kwargs.get('file', sys.stdout).flush()            
# except NameError:
#     pass

# from threading import Thread
# import functools

# def timeout(timeout):
#     def deco(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
#             def newFunc():
#                 try:
#                     res[0] = func(*args, **kwargs)
#                 except Exception as e:
#                     res[0] = e
#             t = Thread(target=newFunc)
#             t.daemon = True
#             try:
#                 t.start()
#                 t.join(timeout)
#             except Exception as je:
#                 print ('error starting thread')
#                 raise je
#             ret = res[0]
#             if isinstance(ret, BaseException):
#                 raise ret
#             return ret
#         return wrapper
#     return deco

# import multiprocessing.pool
# import functools

# def timeout(max_timeout):
#     """Timeout decorator, parameter in seconds."""
#     def timeout_decorator(item):
#         """Wrap the original function."""
#         @functools.wraps(item)
#         def func_wrapper(*args, **kwargs):
#             """Closure for function."""
#             pool = multiprocessing.pool.ThreadPool(processes=1)
#             async_result = pool.apply_async(item, args, kwargs)
#             # raises a TimeoutError if execution exceeds max_timeout
#             return async_result.get(max_timeout)
#         return func_wrapper
#     return timeout_decorator
# import signal 

# import time
# from call_function_with_timeout import SetTimeout


class ConstraintList(list):
    """This class creates a list of constraints"""
    
    def check_if_exists(self, x, ls):
        if x in ls:
            return True
        else:
            return False 

    # Check for some dependencies 
    def contains_constraint(self, constraint, constraint_list):
        if constraint == None: 
            return True
        else:
            constraint_list_str = [str(x) for x in constraint_list]
            match constraint.__class__.__name__:
                # templates that can only occur once in the model
                case 'Init':
                    startswith_ls = [x.startswith('Init') for x in constraint_list_str]
                    return ConstraintList.check_if_exists(self, True, startswith_ls)
                case 'End':
                    startswith_ls = [x.startswith('End') for x in constraint_list_str]
                    return ConstraintList.check_if_exists(self, True, startswith_ls)               
                case _: return False

    def list_to_decl_extension(self, constraint_list, activities):
        output_activities = ""
        output_constraints = ""

        # activities
        for item in activities:
            item_str = "activity " + str(item) + "\n"
            output_activities += item_str

        output1 = ""
        output2 = ""

        for item in constraint_list[:-1]:
            item_str = str(item) + " | | |\n"
            item_str = item_str.replace("(","[")
            item_str = item_str.replace(")","]")
            item_str = item_str.replace(",",", ")
            item_split = re.findall('[A-Z][^A-Z]*', item_str)
            item_str = " ".join(str(item) for item in item_split)
            output1 += item_str

        # last item constraint_list
        item_last_str = str(constraint_list[len(constraint_list)-1]) + " | |"
        item_last_str = item_last_str.replace("(","[")
        item_last_str = item_last_str.replace(")","]")
        item_last_str = item_last_str.replace(",",", ")
        item_split = re.findall('[A-Z][^A-Z]*', item_last_str)
        item_last_str = " ".join(str(item) for item in item_split)
        output2 = item_last_str

        output_constraints = output1 + output2

        output = output_activities + output_constraints

        return output
    

import time
from call_function_with_timeout import SetTimeout
from call_function_with_timeout import SetTimeoutDecorator

    
class LtlList(list):

    def add_first_ltl(self,activities,sigma): ################### discuss with Nicola - assumption declare (activities cannot occur at the same point in time concurrently)
        # sigma = alphabet()
        # activities = ["a","b","c"]

        f = sigma.top()

        for a in activities: 
            activities_except_a = [x for x in activities if x != a]
            a = sigma.proposition(a)

            for b in activities_except_a:
                b = sigma.proposition(b)
                f = f & implies(a,~b)    

        return G(f)        
    
    # def quit_function(self,fct):
    #     # print to stderr, unbuffered in Python 2.
    #     print('{0} took too long'.format(fct), file=sys.stderr)
    #     sys.stderr.flush() # Python 3 stderr is likely buffered.
    #     thread.interrupt_main() # raises KeyboardInterrupt

    # def exit_after(self,s):
    #     '''
    #     use as decorator to exit process if 
    #     function takes longer than s seconds
    #     '''
    #     def outer(fn):
    #         def inner(*args, **kwargs):
    #             timer = threading.Timer(s, LtlList.quit_function, args=[fn.__name__])
    #             timer.start()
    #             try:
    #                 result = fn(*args, **kwargs)
    #             finally:
    #                 timer.cancel()
    #             return result
    #         return inner
    #     return outer

    # @SetTimeoutDecorator(timeout=5)
    def check_consistency(self, constraint, ltl_list, sigma):
        unpacked = sigma.top()
        for c in ltl_list:
            unpacked = unpacked & c
        
        slv = solver()
        xi = scope(sigma)

        f = unpacked & constraint # test consistency by testing the conjunction
        
        st = time.time()
        print("consistency check...")

        result = slv.solve(xi,f,True)
        # p = multiprocessing.Process(target=slv.solve, name="Solver", args=((xi, f, True),))
        # p.start()
        # p.join(60)

        et = time.time()
        print("end consistency check")

        elapsed_time_sec = et - st
        print('Execution time:', elapsed_time_sec, 'seconds')
        
        return result

    # @timeout(5)
    # @SetTimeoutDecorator(timeout=5)
    def check_redundancy(self, constraint, ltl_list, sigma):
        unpacked = sigma.top()
        for c in ltl_list:
            unpacked = unpacked & c
        
        slv = solver()
        xi = scope(sigma)

        f = implies(unpacked,constraint) # test redundancy by testing the negation of the implication

        st = time.time()
        print("redundancy check...")
            
        result = slv.solve(xi,~f,True)
        # p = multiprocessing.Process(target=slv.solve, name="Solver", args=((xi, ~f, True),))
        # p.start()
        # p.join(60)

        et = time.time()
        print("end redundancy check")

        elapsed_time_sec = et - st
        print('Execution time:', elapsed_time_sec, 'seconds')

        return result
    
    # def check_consistency_timeout(self, constraint, ltl_list, sigma):
    #     SetTimeout(LtlList.check_consistency(self, constraint, ltl_list, sigma), timeout=1)
    
    # def check_redundancy_timeout(self, constraint, ltl_list, sigma):
    #     SetTimeout(LtlList.check_redundancy(self, constraint, ltl_list, sigma), timeout=1)
    
# ltl = LtlList()
# sigma = alphabet()
# is_done, is_timeout, erro_message, results = ltl.check_consistency(Init("a"), [ChainPrecedence("b","c"), RespondedExistence("a","b"), CoExistence("c","c")], sigma)

    


    
    # def handler(self, signum, frame):
    #     print("Forever is over!")
    #     raise Exception("end of time")
    


# func = timeout(timeout=5)(LtlList.check_consistency)
# try:
#     func()
# except:
#     pass
