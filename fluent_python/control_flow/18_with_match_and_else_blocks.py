# Context Managers and With Blocks
# Good for removing try ... finally boilerplate 
import sys

class LookingGlass:
    def __enter__(self):
        self.original_write = sys.stdout.write # Save the original sys.stdout.write so we can restore it on exit
        sys.stdout.write = self.reverse_write  # Monkey patch sys.stdout.write with our reverse_write
        return "JABBERWOCY"                    # This gets returned as what
    
    def reverse_write(self, text):          
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please do not divide by zero!")
            return True                       # Return truthy so that the exception is handled and not propegated to the with block
                                              # anything falsy will be propegated (i.e. the exception is not handled in __exit__)
with LookingGlass() as what:
    print("Alice, Kitty, and Snowdrop")
    print(what)

# See contextlib for common context managers and other tools
import contextlib
import sys

@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout = reverse_write
    yield "JABBERWOCY" 
    sys.stdout.write = original_write

# @contextmanager reduces the boilerplate of the class context manager
# Everything before the yield is called during __enter__
# The yield is the return value of __enter__
# The code after yield runs in place of __exit__

# We can add exc handling similar to the original example as follows:
@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout = reverse_write
    msg = ""
    try:
        yield "JABBERWOCY" 
    except ZeroDivisionError:
        msg = "Please do not divide by zero!"
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)

# Case study: using patern matching for a Scheme (lisp dialect) interpreter
# prefix notation e.g.  + x 13 -> x + 13 or define x 13 -> x = 13
# no for or while loops, accomplishes the same through recursion

import math
import operator as op
from collections import ChainMap
from itertools import chain
from typing import Any, TypeAlias, NoReturn

Symbol: TypeAlias = str
Atom: TypeAlias = float | int | Symbol
Expression: TypeAlias = Atom | list

def parse(program: str) -> Expression:
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenize(program))

def tokenize(s: str) -> list[str]:
    """Convert a string to a list of tokens"""
    return s.replace("(", " ( ").replace(")", " ) ").split()

def read_from_tokens(tokens: list[str]) -> Expression:
    """Read an expression from a sequence of tokens"""
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        exp = []
        while tokens[0] != ')':
            exp.append(read_from_tokens(tokens))
        tokens.pop(0)  # discard ')'
        return exp
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return parse_atom(token)

def parse_atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)
        
print(parse("(gcd 18 45)")) # ['gcd', 18, 45]

class Environment(ChainMap[Symbol, Any]):
    """A chain map that allows changing an item in-place"""
    ...
    
# TODO: Continue this example whihc build on case match.

# Using the else block in for, while and try

# for: Runs only when the for loop runs to completion (i.e. not if the for is aborted by break)
# while: The else block will run only if the while condition becomes falsy
# try: will run only if no exception is raised in the try block

my_list = ["apple"]
for l in my_list:
    if l == "bannana":
        break
else:
    raise ValueError("No bannana")

# consider the following example where there is one dangerous call and then another call that does not need to be handled
# try:
#     dangerous_call()
# except OSError:
#     log("OSError")
# else:
#     not_dangerous_call()

