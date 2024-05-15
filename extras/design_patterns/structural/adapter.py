# An adapter provides a different interface for a class ...
# such that it can be used with this class (and others)

# We have two classes that do conceptually the same things but have ...
# different implementations and a different interface.
# We would like to use these together.
from typing import TypeVar, Callable

T = TypeVar("T")

class Candy:
    def unwrap(self):
        print("Unwrapping candy.")

    def eat(self):
        print("Eating candy.")

class Soda:
    def unscrew(self):
        print("Unscrewing the top of the soda bottle.")

    def drink(self):
        print("Drinking the soda.s")

# Lets say that regardless of the interface, we want to call these instances with ...
# prepare
# consume
# or maybe we have an existing class with this interface and want any new interfaces to follow suite
class Adapter:
    def __init__(self, adaptee: T, **adapted_methods: Callable): 
        # It is up to the client in this case to provide a mapping for the new interface
        self.adaptee = adaptee
        self.__dict__.update(**adapted_methods)

    def __getattr__(self, attr):
        getattr(self.adaptee, attr)

    # Just to get some typing
    def prepare(self):
        raise NotImplemented("Do not instantiate the Adapter")

    def consume(self):
        raise NotImplemented("Do not instantiate the Adapter")

if __name__ == "__main__":
    candy = Candy()
    consumable = Adapter(candy, prepare=candy.unwrap, consume=candy.eat)
    consumable.prepare()
    consumable.consume()
    # Now when we get to a part of the codebase where it expects a single interface
    
# This is a pythonic way of creating an adapter (by updating the method at runtime)
# Another option is providing a hardcoded map inside the adapter that needs to be updated ...
# everytime a new class needs adapting.