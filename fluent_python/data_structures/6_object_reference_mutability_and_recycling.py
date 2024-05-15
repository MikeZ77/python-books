# python variables are labels not boxes
a = [1, 2, 3]
b = a # a and b reference the same object
a.append(4)
print(a, b)
# The labels a and b are on the same object

charles = {"name": "Charles L Dodgeson", "born": 1832}
lewis = charles
print(lewis is charles) # True
print(id(lewis), id(charles)) # 139833037328960 139833037328960
# so lewis is an alias for charles

alex = {"name": "Charles L Dodgeson", "born": 1832}
print(alex == charles) # true (because of the __eq__ implementation in dict)
print(alex is charles) # false

x = None
print(x is None)

# The (relative) Mutability of tuples
t1 = (1, 2, [30, 40])
t2 = (1, 2, [30, 40])

print(t1 == t2) # true
print(id(t1[-1]), id(t2[-1]))

t1[-1].append(50)
print(id(t1[-1]))
print(t1 == t2) # False

# Shallow Copy is Default
l1 = [3, [55, 44], (7, 8, 9)]
l2 = list(l1)
print(l2)
print(l1 is l2) # False
print(l1 == l2) # True

# Shallow vs Deep Copy: Seen it many times before
# Note though that deep copy is smart enough to handle cyclical references

# Function Paramaters as References
# In python each param of a function is an alias of the argument passed in
# As a result, the function may change the valuees of any mutable object passed in but it cannot change its reference

def f(a, b):
    print(id(a))
    a += b
    print(id(a))
    return a

x, y = 1, 2
a, b = [1, 2], [3, 4]
print(f(a, b)) # [1, 2, 3, 4]
print(a, b) # [1, 2, 3, 4], [3, 4]

t = (1, 2)
u = (3, 4)
print(f(t, u)) # (1, 2, 3, 4)
print(t, u) # (1, 2) (3, 4)

# Mutable types as default params are a BAD IDEA
class HauntedBus:
    def __init__(self, passengers=[]):
        self.passengers = passengers
    
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = HauntedBus(["Alice", "Bill"])
print(bus1.passengers)
bus1.pick("Charlie")
bus1.drop("Alice")
print(bus1.passengers)
# So far this is fine

bus2 = HauntedBus()
bus2.pick("Carrie")
print(bus2.passengers)
print(bus1.passengers)

bus3 = HauntedBus()
print(bus3.passengers)
# At this point the default is no longer empty
print(bus1.passengers)
# Why is bus1 still a distinct list?
# Thats because if haunted bus does not get a distinct list like for bus1, it reuses the same list

# Defensive programming with mutable paramaters
#E.g. We pass a list and it gets mutated
class TwilightBus:
    def __init__(self, passengers=None):
        if passengers:
            self.passengers = passengers
        else:
            self.passengers = []

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)
        
basektball_team = ["Eric", "Hans", "Alisa"]
bus = TwilightBus(basektball_team)
bus.drop("Hans")

# We probbaly meant to pass a copy of basketball team, becuase we dont want it to be dropped from basektball_team
# Better, the class TwilightBus should make the copy
# self.passengers = list(passengers)

# Del and garbage collection
# Python objects are never explicitly destroyed. But can become unreachable if their label/refernce is removed
# They can then be garbage collected

a = [1, 2]
b = a
del a
print(b) # The object still exists because its ref count is 1 (> 0)
b = [3] # b is rebinded, now it can be garbage collected


