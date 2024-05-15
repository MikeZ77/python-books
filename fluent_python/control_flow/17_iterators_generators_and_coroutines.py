# The Iterator design pattern is built into Python

import re
import reprlib # Used for abrehviated string representations of data structures that can be very large

RE_WORD = re.compile(r"\w+")

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return f"Sentence({reprlib.repr(self.text)})"
    
    
s = Sentence('"The time has come," the Walrus said,')
print(s)
for word in s:
    print(word)

print(s[-2])

# This is a sequence, but why is it iterable with only implementing __len__ and __getitem__ ?
# 1. Checks whether __iter__ is implemented
# 2. If not but __getitem__ is, python creates an iterator that fetches items starting at index 0
# 3. If that fails a TypeError is rasied

class Spam:
    def __getitem__(self, i):
        print("->", i)
        raise IndexError
    
spam_can = Spam()
print(iter(spam_can)) # Builds the iterator from the instance because of __getitem__
print(list(spam_can)) # Builds the iterator and iterats to create the list

from collections import abc
print(isinstance(spam_can, abc.Iterable)) # But not considered iterable sicne it doesnt implement __iter__

class GooseSpam:
    def __iter__(self):
        ...
        
goose_spam = GooseSpam()
print(isinstance(goose_spam, abc.Iterable)) # True
print(issubclass(GooseSpam, abc.Iterable))  # True

# It is better to check if an object is iterable just by calling iter() on it and handling the TypeError
# Because you are probably iterating over the object right after checking it.
# However, if you are holding the item to iterate over it at some other point this could make sense

# Using iter with a Callable
from random import randint

def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1) # 2nd arg is a sentinel/stop value
print(d6_iter) # <callable_iterator object at 0x7f7c84544df0>

for roll in d6_iter:
    # stops at 1
    print(roll)

# Like all iterators it becomes exhausted, and we must rebuild it again using iter()

# Iterables vs Iterators
# Iterators are obtained from iterables
# Consider the simple for loop, Python obtains the iterator behind the scenes. 

s = "abc" # is an iterable
for a in s:
    print(a)

# If we had to try and emulate the behind the scenes of this for ... in syntax, this is what iw would look like
print("---------------------------------")

it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break
    
# The interface for an iterator has two methods:
# __next__
# __iter__

from collections.abc import Iterator
# So an Iterbale has the abstract method __iter__. An iterator is a subclass of Iterable
# which implements __iter__ and has the abstract method __next__

s = ["a", "b", "c"] 
si = iter(s) # Build the iterator from an iterable
# the iterator si implements __next__
print(next(si))
print(next(si))
print(next(si))

try:
    print(next(si))
except StopIteration as ex:
    print(ex)

# A classic implementation of the Iterator design pattern
import re
import reprlib

RE_WORD = re.compile(r"\w+")

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f"Sentence({reprlib.repr(self.text)})"

    def __iter__(self):
        return SentenceIterator(self.words)

class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0
        
    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word
    
    def __iter__(self):
        return self
    
s = Sentence("aa bb cc")
si = iter(s)
sii = iter(si)
print(si is sii) # True

# A pythonic implementation of the same functionality
# Implement using a generator

RE_WORD = re.compile(r"\w+")

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f"Sentence({reprlib.repr(self.text)})"

    def __iter__(self):
        for word in self.words:
            yield word
            
s = Sentence("aa bb cc")
si = iter(s)
print(si) # <generator object Sentence.__iter__ at 0x7f6d9e104ac0>

# Any python function that is a yield keyword in its body is a generator function (or a generator factory)
def simple_gen():
    yield 1
    yield 2
    yield 3

gen = simple_gen() # generator object implement the Iterbale interface
for g in gen:
    print(g)
    
gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen))

# Sentence with a lazy generator
# So far, Sentence has been eager because it builds the list of words right away

RE_WORD = re.compile(r"\w+")

class Sentence:
    def __init__(self, text):
        self.text = text
        
    def __repr__(self):
        return f"Sentence({reprlib.repr(self.text)})"

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
        # OR
        #return (match.group() for match in RE_WORD.finditer(self.text))
            
# Generator expressions

def gen_AB():
    print("start")
    yield "A"
    print("continue")
    yield "B"
    print("end")

# A list comprehension eagerly evaluates
res1 = [x*3 for x in gen_AB()]
print(res1)
res2 = (x*3 for x in gen_AB())
print(res2) # <generator object <genexpr> at 0x7f2e52ae4dd0>
for i in res2:
    print(i)

# As usual, if the generator expression spand more than a couple lines, make it a generator function
# Key take-aways:
# An Iterator implemets __next__ 
# A generator is an iterator built by the python compiler. __next__ is not implement and instead yield is used
# The generator object returned does provide __next__ though, making it an iterator
# So, a generator is an iterator, but an iterator may or may not be a generator

# e.g. range returns a generator, but what if we want something other than intergers
from typing import Generator

class ArithmaticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end
    
    def __iter__(self) -> Generator:
        result_type = type(self.begin + self.step)
        result = result_type(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index