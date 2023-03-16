from pluginbase import PluginBase
import inspect
from lib.abstract import mathematic


plugin_base = PluginBase(package='test.plugins')


plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])

module = plugin_source.load_plugin('add')

instance = module.increment()

print(instance.getName())
print(instance.apply(5))

print(getattr(module, '__name__'))

# print(inspect.getmembers(module))

'''
 This is to list all the classes belong to the module imported above.    
 However, it list not only the class within the module, but also the super class which inherits from the other module.

 So use __subclasses__ for the time being....

'''
classes = [cls_name for cls_name, cls_obj in inspect.getmembers(
    module) if inspect.isclass(cls_obj)]

print(classes)


instance = mathematic.__subclasses__()[0]()
print(instance.apply(6))

'''

for cls in classes:
    print(cls)
    instance = getattr(module, cls)

    print(instance)
'''
