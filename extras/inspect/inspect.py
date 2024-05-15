# Four main use cases: 
# 1. type checking
# 2. getting source code
# 3. inpecting classes and functions 
# 4. information about error traceback


def child_one(a):
    print("Child one")
    return a

def child_two(b):
    print("Child two")
    return b

def child_three(c, d):
    print("Child three")


class Parent:
    def __call__(a):
        print("parent_function")
        b = child_one(a)
        c = child_two(b)
        child_three(c, 2)
      


if __name__ == "__main__":
    import inspect
    from inspect import Parameter
    import sys
    import types
    # print(inspect.getmembers(parent))
    # print(parent.__name__)
    # The second arg is a predicate (typically functions with "is")
    print(inspect.getmembers(Parent(),  inspect.ismethod)) # [('__call__', <bound method Parent.__call__ of <__main__.Parent object at 0x7f4cb877ec50>>)]
    fns = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    for name, fn in fns:
        # Create a function at runtime
        print("code", fn.__code__) # __code__ returns the compiled function
        fn_ = types.FunctionType(fn.__code__, globals(), name)
        setattr(Parent, name, fn_)
    
    print(inspect.getmembers(Parent(), inspect.ismethod))
    Parent().child_one()
    
    print(inspect.getargspec(child_one)) # ArgSpec(args=['a'], varargs=None, keywords=None, defaults=None)
    # So we have bound the functions to the class, but now "self" is being passed as the first arg


    # (_, sample_fn), *_ = fns
    # old_signature = inspect.signature(sample_fn)
    # print(old_signature) # (a)
    # params = [Parameter(param, Parameter.POSITIONAL_ONLY) for param in old_signature.parameters.keys()]
    # new_signature = old_signature.replace(parameters=[Parameter("self", Parameter.POSITIONAL_ONLY), *params])
    # fn_ = types.FunctionType(new_signature, globals())
    # setattr(Parent, fn_.__name__, fn_)

    # Parent().child_one(1)
    

def replace_code(code: str):
    return code.replace("{replaceme}", "{I have been replaced }")

class SomeClass:
    def method_one(self):
        str = "{replaceme} Hello"
        print(str)
        
    def method_two(self):
        str = "Nothing should be replaced here"
        print(str)
        
if __name__ == "__main__":
    
    for name, method in inspect.getmembers(SomeClass, predicate=inspect.isfunction):     
        print(name, method)  
        original_code = inspect.getsource(method)
        updated_code = replace_code(original_code)
        file = inspect.getfile(method)
        compiled_code = compile(updated_code, file, 'exec') 
        namespace = {}
        exec(compiled_code, namespace)
        print(namespace)
