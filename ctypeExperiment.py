from ctypes import *

class POINT(Structure):
     _fields_ = [("x", c_int),
                 ("y", c_int)]

Point2 = type( 'POINT', (Structure,), {
    '_fields_' : [ ("x", c_int),
                   ("y", c_int) ] } )

p2 = Point2(2,3)

import StringIO as sio
s = sio.StringIO()

s.write(buffer(p2))

# FAQ: How do I copy bytes to Python from a ctypes.Structure?

# def send(self):
#     return buffer(self)[:]
# FAQ: How do I copy bytes to a ctypes.Structure from Python?

# def receiveSome(self, bytes):
#     fit = min(len(bytes), ctypes.sizeof(self))
#     ctypes.memmove(ctypes.addressof(self), bytes, fit)
# Their send is the (more-or-less) equivalent of pack, and receiveSome is sort of a pack_into. If you have a "safe" situation where you're unpacking into a struct of the same type as the original, you can one-line it like  memmove(addressof(y), buffer(x)[:], sizeof(y)) to copy x into y. Of course, you'll probably have a variable as the second argument, rather than a literal packing of x.

s.seek(0)
xs = s.read()
print(len(xs))

class Proxy:
    def __init__(self,x):
        self.x = x

    def __getattr__(self,a):
        print("Getting %s" % a )
        return getattr(self.x,a)

p3 = Point2.from_buffer_copy( Proxy(xs ))

