# Inheritance and virutal function test

## inhertitance
<br>
When try to inherit class from parent/child folder, it causes issue in python.  Googled and was told to resolve in the following couple methods:

<li> Add root folder to system environment variable PYTHONPATH (Haven't tried)
<li> Official way is to make self a pip module by creating setup.py (Haven't tried)

<br>

***Since this is not the priority, tentatively move the abstract class into subfolder instead of isolate to somewhere else.***

<br><br>

## multiple inheritance

- https://www.learncodewithmike.com/2020/01/python-inheritance.html

- https://medium.com/seaniap/oop-python-inheritance-%E9%97%9C%E6%96%BC%E7%89%A9%E4%BB%B6%E5%B0%8E%E5%90%91%E7%9A%84%E7%B9%BC%E6%89%BF-f93028056d9b


<br />
<br />

## parameter type hint

   ``` python
   def function (var : <type here>) -> <return type here> :
   ```
<br>
<br>

## private variable/ (and maybe functions)

variable name with __ as beginning seems enforced to be treated as private.  So parent class's self.__xxx  will not be inherit by child.


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
