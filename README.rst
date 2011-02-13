µrecord
=======

``Record`` is a simple metaclass for creating classes whose instances are
designed to hold a fixed number of named fields. It's similar to
``collections.namedtuple()`` in its operation, only it uses metaclasses rather
than string formatting and ``exec``.

    >>> import math
    >>> from urecord import Record

    >>> class CartesianPoint(Record('x', 'y')):
    ...     def to_polar(self):
    ...         angle = math.atan2(self.y, self.x)
    ...         radius = math.sqrt(self.x ** 2 + self.y ** 2)
    ...         return PolarPoint(angle, radius)

    >>> class PolarPoint(Record('angle', 'radius')):
    ...     def to_cartesian(self):
    ...         x = self.radius * math.cos(self.angle)
    ...         y = self.radius * math.sin(self.angle)
    ...         return CartesianPoint(x, y)

    >>> p1 = CartesianPoint(3, 4)
    >>> p1
    CartesianPoint(x=3, y=4)
    >>> p2 = p1.to_polar()
    >>> p2
    PolarPoint(angle=0.927..., radius=5.0)
    >>> p2._replace(angle=0.25)
    PolarPoint(angle=0.25, radius=5.0)
    >>> p2._asdict()
    {'radius': 5.0, 'angle': 0.927...}

(Un)license
===========

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
