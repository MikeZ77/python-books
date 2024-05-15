# A class that is a collection of fields, with little to no extra functionality
# Class builders are a shortcut to creating data classes

# Consider the simple class
class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

from collections import namedtuple

Coordinate = namedtuple("Coordinate", "lat lon")
print(issubclass(Coordinate, tuple))
moscow = Coordinate(55.576, 37.613)
print(moscow) # Useful __repr__
print(moscow == Coordinate(lat=55.576, lon=37.613)) # Meaningful __eq__

import typing

# Includes types
Coordinate = typing.NamedTuple("Coordinate", [("lat", float), ("lon", float)])
Coordinate = typing.NamedTuple("Coordinate", lat=float, lon=float)
print(issubclass(Coordinate, tuple))
print(typing.get_type_hints(Coordinate))

# As a class, makes it easier to override or add methods
class Coordinate(typing.NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = "N" if self.lat >=0 else "S"
        we = "E" if self.lon >=0 else "W"
        return f"{abs(self.lat):.1f}*{ns}, {abs(self.lon):.1f}*{we}"
    
# As a dataclass, you get more generated methods
from dataclasses import dataclass
@dataclass(frozen=True) # frozen=True makes the fields immutable 
class Coordinate():
    lat: float
    lon: float

    def __str__(self):
        ns = "N" if self.lat >=0 else "S"
        we = "E" if self.lon >=0 else "W"
        return f"{abs(self.lat):.1f}*{ns}, {abs(self.lon):.1f}*{we}"
    
# Both ways can construct a dict
from dataclasses import asdict

coord = Coordinate(1, 2)
print(asdict(coord))

Coordinate = typing.NamedTuple("Coordinate", lat=float, lon=float)
coord = Coordinate(1, 2)
print(coord._asdict())

# More on classic named tuples
# A factory that builds subclasses of tuple with field names, a class name, and a __repr__
from collections import namedtuple
City = namedtuple("City", "name country population coordinates")
tokyo = City("Tokyo", "JP", 36.933, (35.435, 139.535))
print(tokyo)
print(tokyo.population)

print(City._fields)
Coordinate = namedtuple("Coordinate", "lat, lon")
delhi_data = ("Delhi NCR", "IN", 21.955, Coordinate(27.434535, 35.466667))
delhi = City._make(delhi_data)
print(delhi)
print(delhi._asdict())

import json
print(json.dumps(delhi._asdict()))

# Give the nameduple defaults (default values for each of the N rightmost fields)
Coordinate = namedtuple("Coordinate", "lat, lon, reference, country", defaults=["WGS84", "CA"])
coord = Coordinate(lat=1, lon=2)
print(coord)
print(Coordinate._field_defaults)

# More on NamedTuples
from typing import NamedTuple, Optional

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = "WGS84"

# A brief into to type hints
# not enforced by the bytecode compiler and interpreter (not enforced at runtime)
# documentation that can be verified by IDE's and type checkers
# There are static type checkers (mypy) that check python source code at rest

class SomeClass(NamedTuple):
    a: str           # A concrete class
    b: list[int]     # A paramaterized collection type
    c: Optional[str] # An Optional type
    d: int = 12      # Init with a value

class DemoNTClass(typing.NamedTuple):
    a: int
    b: float = 1.1
    c = "spam"

# a is a class attribute and is also made an instance attribute
# b is a class attribute that is made an instance attribute with default
# c is just a regular class attribute
# a and b have annotations

print(DemoNTClass.__annotations__)
print(DemoNTClass.a)
print(DemoNTClass.b)
print(DemoNTClass.c)

# For now, we can think of the class attributes a and b as property getters
# I.e. methods that dont require a call () to retrieve an instance attribute
from dataclasses import dataclass, field

# Data Class
@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
    athlete: bool = field(default=False, repr=False)
# If we just set a default [], then every instance of ClubMember will reference the same list which is not what we want
# field init as instance attribute

# Dataclass inheritance
@dataclass
class HackerClubMember(ClubMember):
    all_handles = set() # Just a class attribute, if we add a type annotation, dataclass will find it and make it an instance field
    handle: str = ""

    def __post_init__(self): # Added to the last part of __init__ (common use is for validation and computing fields based on other fields)
        cls = self.__class__
        if self.handle == "":
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            msg = f"handle {self.handle} already exists"
            raise ValueError(msg)
        cls.all_handles.add(self.handle)

anna = HackerClubMember("Anna Ravenscroft", handle="AnnaRaven")
print(anna) # HackerClubMember(name='Anna Ravenscroft', guests=[], handle='AnnaRaven')
leo = HackerClubMember("Leo Rachel")
print(leo) # HackerClubMember(name='Leo Rachel', guests=[], handle='Leo')
print(HackerClubMember.all_handles) # {'Leo', 'AnnaRaven'}

# In summary:
# name is a field because it has a type annotation
# guests is a field because it has a type annotation and a new list is created for each ClubMember
# athlete is a field but will not be shown in print statements
# all_handles is not a field
# handle is a field

# What if we want to pass arguments to init that are not to be used as fields?
# These are called init-only variables 
#E.g. a data class whos fields are init from a datbase record, but we need to pass in the DB object
from dataclasses import InitVar

@dataclass
class C:
    i: int
    j: int = None
    database: InitVar[object] = None
def __post_init__(self, database):
    if self.j is None and database is not None:
        self.j = database.lookup("j")

# c = C(10, database=my_database) => database class var is set but no as a instance field

#Typical example of dataclass
from dataclasses import dataclass, field, fields
from typing import Optional
from enum import Enum, auto
from datetime import date

class ResourceType(Enum):
    BOOK = auto()
    EBOOk = auto()
    VIDEO = auto()

@dataclass
class Resource:
    """ Media resource description """
    identifier: str
    title: str = "<untitled>"
    creators: list[str] = field(default_factory=list)
    date: Optional[date] = None
    type: ResourceType = ResourceType.BOOK
    description: str = ""
    language: str = ""
    subjects: list[str] = field(default_factory=list)

    # tag::REPR[]
    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__name__
        indent = ' ' * 4
        res = [f'{cls_name}(']                            # <1>
        for f in fields(cls):                             # <2>
            value = getattr(self, f.name)                 # <3>
            res.append(f'{indent}{f.name} = {value!r},')  # <4>

        res.append(')')                                   # <5>
        return '\n'.join(res)                             # <6>
# end::REPR[]

book_default = Resource('0')
description = 'Improving the design of existing code'
book = Resource('978-0-13-475759-9', 'Refactoring, 2nd Edition',
                ['Martin Fowler', 'Kent Beck'], date(2018, 11, 19),
                ResourceType.BOOK, description,
                'EN', ['computer programming', 'OOP'])

print(book_default)
print(book)

import typing

class City(typing.NamedTuple):
    continent: str
    name: str
    country: str

cities = [
    City('Asia', 'Tokyo', 'JP'),
    City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),
    City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]

def match_asian_cities():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia'):
                results.append(city)
    return results

print(match_asian_cities())