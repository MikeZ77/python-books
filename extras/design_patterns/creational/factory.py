from typing import Protocol

class Pizza(Protocol):  
    def get_toppings() -> tuple: ...


class GreekPizza:
    def get_toppings():
        return ("Olives", "Feta", "Pepperoni")

class PepperoniPizza:
        def get_toppings():
            ("Pepperoni",)
        

def create_pizza(pizza: str) -> Pizza:
    """Factory"""
    pizzas = {
        "Pepperoni": PepperoniPizza,
        "Greek": GreekPizza,
    }

    return pizzas[pizza]()


# The goal: isolate the creation of the object from the code that needs it

# The Simple Factory (Pattern)
# Techincally not a true pattern
# Encapsulates object creation in one place
# Reduces duplicate code by enforcing DRY


# Suppose we had some logic in our application:
# Maybe these are controllers for http endpoints, and part of the payload is the type
# You need to create the pizza model (object) before inserting into the database
def send_order(pizza: str):
    """Maybe this inserts the pizza info into the database"""
    if pizza == "Pepperoni":
        return PepperoniPizza()
    elif pizza == "Greek":
        return GreekPizza()
    else:
        raise ValueError("No such pizza exists")

# Then some copletely seperate part of the codebase also crates a new pizza
def bill_pizza(pizza: str):
    """Maybe this creates a pizza so it can be used for blling"""
    if pizza == "Pepperoni":
        return PepperoniPizza()
    elif pizza == "Greek":
        return GreekPizza()
    else:
        raise ValueError("No such pizza exists")


# So the basic point about this simple factory is reducing code duplication and keeping DRY
# Also, every time a new pizza is added or removed from the available pizzas, we can just update the factory ...
# instead of every place in the code.
# Note that if there are not multiple points in the coding when your are checking which object to instantiate ...
# Then I dont see any point in using this pattern

 
# The Abstract Factory
# We have A group of of factories that have a common theme that are based on an ABC
# The client creates a concrete implementation of the factory
# And then uses the generic interface of the factory to create the concrete objects that are part of the theme

from abc import ABC, abstractmethod

class PizzaFactory(ABC):
    # Lets treat toppings like some global configuration that gets loaded from json or a database
    toppings = {"pepperoni": {"is_vegan": False}, "feta": {"is_vegan": False}, "mozzerela": {"is_vegan": False}, "olives": {"is_vegan": True}}
    
    @abstractmethod
    def create_pizza(self, pizza): ...
    
class Pizza(ABC):
    toppings: list
    crust: str
    price: float

    def __repr__(self):
        return f"{self.__class__.__name__}({self.toppings=}, {self.crust=})"


class Pepperoni(Pizza):
    def __init__(self, crust, toppings=["pepperoni", "mozzerela"]):
        self.toppings = toppings
        self.crust = crust
        self.price = 7.99
        
class Greek(Pizza):
    def __init__(self, crust, toppings=["feta", "olives"]):
        self.toppings = toppings
        self.crust = crust
        self.price = 8.99
    
class CreateStandardPizza(PizzaFactory):
    """Knows how to take any pizza and make it standard"""
    def create_pizza(self, pizza: Pizza):
        return pizza("standard")

class CreateVeganPizza(PizzaFactory):
    """Knows how to take any pizza and make it vegan"""
    def create_pizza(self, pizza: Pizza):
        # Lets just assume the vegan pizzas all use the standard crust
        pizza_ = pizza("standard")
        pizza_.toppings = [topping for topping, config in self.toppings.items() if config["is_vegan"]]
        pizza_.price *= -0.9
        return pizza_
    
class CreateThinCrustPizza(PizzaFactory):
    """Knows how to take any pizza and make it vegan"""
    def create_pizza(self, pizza: Pizza):
        pizza_ = pizza("thin")
        pizza_.price *= 1.2
        return pizza_

if __name__ == "__main__":
    # Init our factories
    standard = CreateStandardPizza()
    vegan = CreateVeganPizza()
    
    # We pass a factory a type it knows how to handle
    # a Piazza factory should know how to handle a pizza type
    standard_pepperoni = standard.create_pizza(Pepperoni)
    vegan_greek = vegan.create_pizza(Greek)
    
    print(standard_pepperoni)
    print(vegan_greek)

    
# Basically the usefulness of this is that we have factories that are less likely to change ...
# but can be added or removed so long as they know how to use the Pizza interface
# Also, we can easily new Pizza types so long as they implement the Pizza interface

# I think one of the key takeaways from both these examples is that the factory encapsulates some busines logic ...
# that it knows how to work with, and the client doesnt need to know anything about it.

# For example, even in the simple factory pattern, we could pass it some Config object which implements a Config interface ...
# and the instantiation or handling of the returned object can be handled by the factory based on this config.






