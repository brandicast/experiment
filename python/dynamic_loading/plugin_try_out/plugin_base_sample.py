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
