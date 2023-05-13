# Inheritance and virutal function test

## inhertitance
<br>
When try to inherit class from parent/child folder, it causes issue in python.  Googled and was told to resolve in the following couple methods:

<li> Add root folder to system environment variable PYTHONPATH (Haven't tried)
<li> Official way is to make self a pip module by creating setup.py (Haven't tried)

<br>

***Since this is not the priority, tentatively move the abstract class into subfolder instead of isolate to somewhere else.***

<br>

## parameter type definition

<br>

Python has no strict type definition in terms of parameters pass in and return.  Everything is an object.   However, in order to let people understand before runtime, after Python 3.x, can take note for type such as:

```python
    def apply(self, image_array: cv2.Mat) -> cv2.Mat:
```

where image_array is reminded as type of cv2.Mat, as well as return the same cv2.Mat

<br>

## virtual function
<br>
There's no actual virtual function concept in python.  The alternative way is to create an abstract class by raising exception if the class is being called without override, such as:

<br>

```python
class virtualClass:
   def __init__(self):
       pass
   def virtualMethod(self): #virtual function.
       raise NotImplementedError( "virtualMethod is virutal! Must be overwrited." )

class subClass( virtualClass ):
   def __init__(self):
       virtualClass.__init__(self)
       pass
   def virtualMethod(self): #overwrite the virtual function.
       print 'subClass! have overwirted the virtualMethod() success.'
```
