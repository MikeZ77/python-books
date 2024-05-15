print("Importing package pkg1 ...")

def say_hi():
    print("Hello")
    
import pkg1.pkg2.mod2
from pkg1.pkg2.mod2 import say_hi as say_hi_mod2

# def this_func_should_not_be_exported():
#     ...