

from abc import ABC


class SimpleProperty:
    def __init__(self):
        self._value = None
    
    def __set_name__(self, obj, name):
        print(f"setname self={self} obj={obj} name={name}")
        self._name = name

    def __get__(self, obj , b):
        print(f"get a={a} b={b}")
        return self._value

    def __set__(self, obj, v, *args):
        print(f"set obj={obj}, v={v} args={args}")
        obj._value = v


class Foo:
    a = SimpleProperty()
    b = SimpleProperty()

    def __init__(self):
        self.a  = 10
        self.b = 20

        #self.c = 10
        #self.d = 20

f = Foo()
        
        
        
