'''
works but discouraged by PEP 302

use importlib instead....refer to importlib_sample_final.py
'''


plugin = __import__("plugins.add", fromlist=('add',))

print(type(plugin))
print(plugin.__name__)
#my_class = getattr(plugin, "increment")
my_class = plugin.increment()

print(my_class.apply(5))
