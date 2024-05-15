if __name__ == "__main__":
    # A metaclass defines how the class is constructed as opposed to the instance.
    class SingletonMeta(type):
        __instance = None

        def __call__(cls, *args, **kwargs):
        # In the metaclass, __call__ gets called when an instance of a metaclass is called (Singleton)
        # https://vetude.com/__call__-in-pyhon-metaclass/
            if not cls.__instance:
                instance = super().__call__(*args, **kwargs) 
                cls.__instance = instance
            return cls.__instance
        
    class Singleton(metaclass=SingletonMeta):
        def __init__(self):
            self._state = {}
            
        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, value: dict):
            self._state.update(value)
            
    my_singleton_one = Singleton()
    my_singleton_one.state = {"1": "Update one"}
    my_singleton_two = Singleton()
    my_singleton_two.state = {"2": "Update two"}
    
    print(my_singleton_one.state, my_singleton_two.state)
    
else:
    class Singleton:
        def __init__(self):
            self._state = {}
            
        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, value: dict):
            self._state.update(value)
    
    my_singleton = Singleton()



