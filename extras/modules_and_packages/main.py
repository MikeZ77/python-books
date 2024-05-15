import module1

print(globals()["module1"]) # <module 'module1' from '/home/mzaghi/fluent_python/extras/modules_and_packages/module1.py'>

# A module is an object like everything else in python
m = globals()["module1"]
print(type(m))
print(hex(id(m)))

import types

mod = types.ModuleType("mod", "This is a test module")
my_mod = mod
print(hex(id(my_mod)), hex(id(mod)))

import module1 as some_mod # alias
print(hex(id(module1)), hex(id(some_mod)))

print(dir(module1)) # dir shows the attributes of the module
# here my_func and x are included since we imported module1

# This a shortcut reference for globals()["module1"]
import module1
assert module1 is globals()["module1"]

print(module1.__dict__) # we can see we get all the built ins
print(module1.__name__)
print(module1.__file__)

module1.__dict__["my_func"]()

# Like it is mentioned in the readme, a python module can be written in C or C++
import socket, math

# math is a built-in, so it is written in C
# socket is part of the standard library, so it is written in python
print(socket, math) 

import sys

# Python has finders (job is to find a module) and loaders (job is to load that found module)
print(sys.meta_path) # meta path shows a list of finders
# An importer is both a finder and a loader

importer = sys.meta_path[0] # BuiltinImporter used for built-in modules (compiled into the python interpreter)
# print(sys.builtin_module_names)
# print(importer)

# For some reason this importer is not available in meta_path
from importlib.machinery import BuiltinImporter, PathFinder

import itertools
print(itertools) # <module 'itertools' (built-in)>

spec = BuiltinImporter().find_spec('itertools')
print(spec) # Found it: ModuleSpec(name='itertools', loader=<class '_frozen_importlib.BuiltinImporter'>, origin='built-in')

# Says to use loader loader=<class '_frozen_importlib.BuiltinImporter'>
loaded_itertools = spec.loader.load_module('itertools')
print(loaded_itertools)
print(loaded_itertools.chain)

# PathFinder will look for python modules in sys.path
print(sys.path)

# The process from the begining:
"""
import sys, socket, module1
1. Check if the module is cached: sys.modules['points']
2. If it is not found then a loader is used and the module object is created in memory and added to sys.modules
3. When we import we get a reference to the module object and it is added to globals()
"""

# Lets see how to import a module ourselves without import
import sys
import types

module_name = "my_custom_module"
module_file = "/home/mzaghi/fluent_python/extras/modules_and_packages/module1.py"

mod = types.ModuleType(module_name)
mod.__file__ = module_file

# Add to the sys.moduels cache (first place checked when importing)
sys.modules[module_name] = mod

# IDEA: could you store code in a DB and compile/execute it as a module?
with open(module_file, "r") as code_file:
    source_code = code_file.read()
    print(source_code)
    
# first compile the source code
code = compile(source_code, module_file, "exec") 
# Note that when the module is compiled, it is not just on object that is created
# All globally defined variables like functions and classes are also created (in this case my_func)
exec(code, mod.__dict__) # where to store globals

mod.my_func()

# Now, say we do the following import
from module1 import my_func # my_func only references the my_func obj in memory
# However the full module is loaded into sys.modules (we just dont have a reference to it). There is no partial loading.

from module1 import * 
# will create refernces of everyting in module1 in the current namespace (globals)
# This can be a bad idea, sance any object in module1 would override an object in main with the same name


# We saw that we have __file__ and __name__ in each modules global namespace
print(__name__) # note that we get "__main__"

import module1
print(module1.__name__) # note that we get "module1"

# So, when a module gets run (like it is the entrypoint) it gets named as __main__


# Packages are a way of structuring pythons module namespaces (globals or locals)
import collections, socket

# Here, collections is a package while socket is a module
# We still get a module object for both, however, collections has __path__ which points to where the package code resides
print(collections.__path__)
# print(collections.__path__, socket.__path__) # AttributeError: module 'socket' has no attribute '__path__'

# We create pkg1 with an __init__.py inside it. A package is defined as a directory with a __init__.py
# The package name is the same as the directory name

import pkg1

# Here python uses PathFinder to locate pkg1 by going through all the paths in sys.path
print(sys.path)

# Note that '/home/mzaghi/fluent_python/extras/modules_and_packages' is the first entry in sys.path.
# Thats because python will add you're current directory as the first path by default, and pkg1 lives in modules_and_packages
# Note that this is what happens when I run F5 (I guess vscode debug cd's to the directory the file resides automatically)

# However, if I tried to import pkg1 from the root directory, the pathfinder would not find it because it does not exist in sys.path
pkg1.say_hi()
print(pkg1.__path__) # ['/home/mzaghi/fluent_python/extras/modules_and_packages/pkg1']
print(pkg1.__package__) # pkg1
print(pkg1.__spec__)
#ModuleSpec(name='pkg1', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7fdf39eee110>, origin='/home/mzaghi/fluent_python/extras/modules_and_packages/pkg1/__init__.py', submodule_search_locations=['/home/mzaghi/fluent_python/extras/modules_and_packages/pkg1'])

# Now we add a module mod1
import pkg1

print(globals()["pkg1"])
print(sys.modules["pkg1"])

try:
    pkg1.mod1
except AttributeError as exc:
    # Note that importing package does not import the modules inside it
    print(exc)

# This is how:
import pkg1.mod1

# Note that this first imports pkg1 (runs __init__.py) then import mod1
print("pkg1" in globals()) # True
print("mod1" in globals()) # False
print("pkg1.mod1" in globals()) # False

# So there is not seperate symbol/reference for mod1. You can only reference it from pkg1 this way.
# But we could do it like this:

from pkg1 import mod1
print("mod1" in globals()) # True

# Now lets create another packages inside pkg1 
import pkg1.pkg2.mod2

print("pkg1.pkg2" in sys.modules)
print("pkg1.pkg2.mod2" in sys.modules)

import pkg1.pkg2.mod2 as mod
mod.say_hi()

# Now we add import pkg1.pkg2.mod2 to __init__.py, we can just import like this to get access
import pkg1

pkg1.pkg2.mod2.say_hi()

# Now I want to expose the mod2 say_hi directly ...
# from pkg1.pkg2.mod2 import say_hi as say_hi_mod2
import pkg1
pkg1.say_hi_mod2()

# These are examples or absoulte imports (from sys.path)
# We can also use relative imports from the file

# from . import pkg1 # Error: We cannot use relative imports outside a package

# . cur dit
# .. parent dir

# Some other useful info:
from pkg1 import *
# While python does not have a direct way to make objects private, we can use _some_func s.t. it will not
# be imported when from pkg1 import * is used

# Also, we can specifiy which modules/objects should be imported inside __init__.py
# e.g. __all__ = ["say_hi"]

# We can also run python packages from the command line using the -m option
# cd modules_and_packages/
# python -m server.app

# Instread of specifying server.app, we can also create a __main__ as an entry point
# python -m server

# note that -m stands for module. Its basically the same as creating a .py file and having import server
# the python http.server is run this way using a __main__ file. python -m http.server