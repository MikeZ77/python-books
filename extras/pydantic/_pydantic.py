# # pydantic enforces the types we specify for our models at runtime
# # gives data validation

# from pydantic import BaseModel, ValidationError

# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     age: int

# p = Person(first_name="Isac", last_name="Newton", age=84)
# print(p)
# try:
#     p = Person(first_name=100, last_name=200, age="3")
# except ValidationError as ex:
#     print(ex)
    
# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     age: int = None


# p = Person(first_name="Isac", last_name="Newton")

# # Serialize this model to a python dictionary
# pd = p.model_dump()
# print(pd)

# pj = p.model_dump_json()
# print(pj)

# pde = p.model_dump(exclude={"age"})
# print(pde)

# pji = p.model_dump_json(include={"first_name", "age"}, indent=4)
# print(pji)

# from datetime import date

# # Can aslso deserialize
# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     dob: date
    
# data = {
#     "first_name": "Isaac",
#     "last_name": "Newton",
#     "dob": date(1643, 1, 4)
# }  

# p = Person.model_validate(data)
# print(p)

# # Works as well
# data = {
#     "first_name": "Isaac",
#     "last_name": "Newton",
#     "dob": "1643-01-04"
# }  

# p = Person.model_validate(data)
# print(p)

# # Can use json

# json = """
#     {
#         "first_name": "Isaac",
#         "last_name": "Newton",
#         "dob": "1643-01-04"
#     }
# """

# p = Person.model_validate_json(json)
# print(p)

# # Typically, for json we use camelCase for fields, not snake_case
# from pydantic import Field
# # We can use Field to expand how we define a field in our class

# class Person(BaseModel):
#     first_name: str = Field(default=None, alias="firstName")
#     last_name: str = Field(default=None, alias="lastName")
#     dob: date = None

# p = Person.model_validate(data)
# print(p.model_dump()) # {'first_name': None, 'last_name': None, 'dob': datetime.date(1643, 1, 4)}
# print(p.model_dump_json()) # {"first_name":null,"last_name":null,"dob":"1643-01-04"}

# # Problem, default sets this as None becuase its looking for camelCase. If we did not have default it would throw a ValidationError
# class Person(BaseModel):
#     first_name: str = Field(default=None, alias="firstName")
#     last_name: str = Field(default=None, alias="lastName")
#     dob: date = None
    
#     class Config:
#         populate_by_name = True


# p = Person.model_validate(data)
# print(p.model_dump()) # {'first_name': 'Isaac', 'last_name': 'Newton', 'dob': datetime.date(1643, 1, 4)}
# print(p.model_dump_json()) # But now we want to use the alias/camelCase on our dump
# print(p.model_dump_json(by_alias=True)) # {"firstName":"Isaac","lastName":"Newton","dob":"1643-01-04"}


# Note: At this point I swtiched to pydantic v1
from datetime import date
from pydantic import BaseModel, ValidationError, Field

class Person(BaseModel):
    first_name: str = Field(alias='firstName', default=None)
    last_name: str = Field(alias='lastName')
    dob: date = None
        
    class Config:
        allow_population_by_field_name = True

data = {
    'firstName': 'Isaac',
    'lastName': 'Newton',
    'dob': date(1643, 1, 4)
}

data_junk = {**data, "junk": "extraneous field"}
p = Person.parse_obj(data_junk)
print(p) # first_name='Isaac' last_name='Newton' dob=datetime.date(1643, 1, 4)

# default behavior, "junk" is ignored
print(hasattr(p, "first_name")) # True
print(hasattr(p, "junk")) # False

# Other options, add it, or raise an error:
from pydantic import Extra

class Person(BaseModel):
    first_name: str = Field(alias='firstName', default=None)
    last_name: str = Field(alias='lastName')
    dob: date = None
        
    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
        
p = Person.parse_obj(data_junk)
print(p) # first_name='Isaac' last_name='Newton' dob=datetime.date(1643, 1, 4) junk='extraneous field'

# More typical, do not allow it. We probably want to know about it.
class Person(BaseModel):
    first_name: str = Field(alias='firstName', default=None)
    last_name: str = Field(alias='lastName')
    dob: date = None
        
    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


# There is an easier way to specify field aliases
def snake_to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("value must be a string")
    words = value.split("_")
    value = "".join(word.title() for word in words if word)
    return f"{value[0].lower()}{value[1:]}"

print(snake_to_camel_case("my_first_name"))

class CustomBaseModel(BaseModel):
    class Config:
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True # We want to be able to work with snake_case
        extra = Extra.forbid
        
        
class Person(CustomBaseModel):
    first_name: str = None
    last_name: str
    dob: date = None

p = Person(first_name="Isaac", last_name="Newton", dob=None)
print(p)  
print(p.json(by_alias=True))

# Field Validations
from pydantic import conint

class Test(CustomBaseModel):
    age: conint(gt=0, le=150)


from pydantic import constr

class Test(CustomBaseModel):
    first_name: str = None
    last_name: constr(strip_whitespace=True, strict=True, min_length=2, curtail_length=25) # strict=True => do not cast to str if it is possible

t = Test(last_name="My            Newton             Is this here?")
print(t)
    
    
# If pydantics built in validators are not sufficient, we can implement our own
print(Test(last_name="*" * 200))

from pydantic import validator

# class Test(CustomBaseModel):
#     hash_tag: str
    
#     @validator("hash_tag")
#     def validate_hash_tag(cls, value):
#         if not value.startswith("#"):
#             raise ValueError("Hash must start with a #")
#         return value.lower()


# p = Test(hash_tag="#aaaaaa")
# print(p)
# try:
#     p = Test(hash_tag="aaaaaa")
# except ValueError as ex:
#     print(ex)    

class Test(CustomBaseModel):
    hash_tag: constr(min_length=5, strip_whitespace=True)

    @validator("hash_tag")
    def validate_hash_tag(cls, value):
        if not value.startswith("#"):
            return f"#{value.lower()}"
        return value.lower()

try:
    p = Test(hash_tag="#A")
except ValidationError as ex:
    # The string validation gets triggered first before the custom validation
    print(ex)
    
from enum import Enum
from typing import List, Tuple, Union

class PolygonType(Enum):
    triangle = 3
    tetragon = 4
    pentagon = 5
    hexagon = 6

t = PolygonType.triangle
print(t.name, t.value)

class PolygonModel(CustomBaseModel):
    polygon_type: PolygonType
    vertices: List[Tuple[Union[int, float], Union[int, float]]]
    
    # Note that the validator runs on vertices regardless if polygon_type is validated
    @validator("vertices")
    # value=vertices value , values=all other fields in a dict
    def validate_vertices(cls, value, values):
        polygon_type = values.get("polygon_type")
        if polygon_type:
            num_vertices_required = polygon_type.value
            if len(value) != num_vertices_required:
                raise ValueError("Number of vertices provided does not match number of verices required")
        return value
    
p = PolygonModel(polygon_type=PolygonType.triangle, vertices=[(1, 1), (2, 2), (3, 3)])
print(p)

# Create models composed of other models with full serialization and deserialization
class Author(CustomBaseModel):
    first_name: constr(min_length=1, max_length=20, strip_whitespace=True)
    last_name: constr(min_length=1, max_length=20, strip_whitespace=True)
    display_name: constr(min_length=1, max_length=25) = None

    # always = True forces the validator to run, even if display_name is None, this
    # is how we can set a dynamic default value
    @validator("display_name", always=True)  
    def validate_display_name(cls, value, values):
        # Construct the display name if it has not been provided
        if not value and 'first_name' in values and 'last_name' in values:
            first_name = values['first_name']
            last_name = values['last_name']
            return f"{first_name} {(last_name[0]).upper()}"
        return value

a = Author(first_name="Gottfried", last_name="Leibniz")
print(a)

from pydantic import conlist

class Post(CustomBaseModel):
    byline: conlist(item_type=Author, min_items=1)
    title: constr(min_length=10, max_length=50, strip_whitespace=True)

    @validator("title")
    def validate_title(cls, value):
        return value and value.title()