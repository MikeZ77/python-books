from singleton import my_singleton

my_singleton.state = {"1": "updated by client 1"}

from singleton_client_2 import my_singleton

# We can see that singleton_client_2 updated the same object ...
# This is because the singleton module gets loaded once and cached in sys.modules
print(my_singleton.state)
# {'1': 'updated by client 1', '2': 'updated by client 2'}


