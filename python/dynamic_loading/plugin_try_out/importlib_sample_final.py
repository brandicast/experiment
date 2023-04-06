'''
https://myapollo.com.tw/blog/python-pkgutil-importlib/

THIS DOESN'T WORK YET.    THOUGH, IT CAN STILL GO FURTHER TO USE inspect.getmembers TO DIG FURTHER.   BUT JUST TOO BOTHERSOME.   
WILL JUST USE TOOL

'''
import pkgutil
import importlib

from pathlib import Path
from lib.abstract import mathematic

'''
def load_modules():
    """
    Import all classes under the folder 'modules'.
    >>> load_modules()
    """
    for finder, name, _ in pkgutil.iter_modules(['plugins']):
        try:
            print('{}.{}'.format(finder.path, name))
            #importlib.import_module('{}.{}'.format(finder.path, name))
            importlib.import_module('{}.{}'.format("plugins", name))

        except ImportError as e:
            print(e)


load_modules()

'''

pkg = 'plugins'

iter = pkgutil.iter_modules([pkg])

plugins = []
for item in iter:
    plugin = importlib.import_module('{}.{}'.format(pkg, item.name))

for module in mathematic.__subclasses__():
    instance = module()
    print(instance.apply(5))

'''
plugins = []
for item in iter:
    print(item)
    print(type(item))
    print(item.module_finder.path)
    print(item.name)

    plugin = importlib.import_module('{}.{}'.format("plugins", item.name))
    plugins.append(plugin)

    for i in dir(plugin):
        print(i)
        print(type(getattr(plugin, i)).__name__)
    print('---------------------------------')
'''
