class Record(type):
    """
    A metaclass for creating structured records.

    :class:`~urecord.Record` is a simple metaclass for creating classes whose
    instances are designed to hold a fixed number of named fields. It's similar
    to :func:`collections.namedtuple` in its operation, only it uses
    metaclasses rather than string formatting and ``exec``.

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
    """

    def __new__(mcls, *properties, **kwargs):
        attrs = {'_fields': properties}

        for i, prop in enumerate(properties):
            attrs[prop] = property((lambda i: lambda obj: obj[i])(i))

        name = kwargs.get('name')
        if name is None:
            name = 'Record(' + ', '.join(map(repr, properties)) + ')'
        attrs['__name__'] = name

        return type(name, (RecordInstance,), attrs)


class RecordInstance(tuple):

    def __new__(cls, *args, **kwargs):
        """
        Create a new :class:`RecordInstance`.

        This method allows you to use both positional and keyword arguments to
        create the record::

            >>> Point = Record('x', 'y', name='Point')

            >>> Point(1, 2)
            Point(x=1, y=2)

            >>> Point(1, y=2)
            Point(x=1, y=2)

            >>> Point(x=1, y=2)
            Point(x=1, y=2)

        It will also raise a :exc:`TypeError` if the provided arguments are
        invalid.

            >>> Point(1, 2, 3)
            Traceback (most recent call last):
            ...
            TypeError: Expected 2 values, got 3

            >>> Point(1)
            Traceback (most recent call last):
            ...
            TypeError: Expected 2 values, got 1

            >>> Point(1, z=3)
            Traceback (most recent call last):
            ...
            TypeError: Unexpected argument 'z'

            >>> Point(a=12)
            Traceback (most recent call last):
            ...
            TypeError: Expected 2 values, got 1
        """
        if not kwargs:
            if len(args) != len(cls._fields):
                raise TypeError("Expected %d values, got %d" % (
                    len(cls._fields), len(args)))
            return tuple.__new__(cls, args)

        unassigned = object()
        slots = [[field, unassigned] for field in cls._fields]

        if len(args) + len(kwargs) != len(cls._fields):
            raise TypeError("Expected %d values, got %d" % (
                len(cls._fields), len(args) + len(kwargs)))

        for i, value in enumerate(args):
            slots[i][1] = value

        for key, value in kwargs.iteritems():
            if key not in cls._fields:
                raise TypeError("Unexpected argument %r" % key)
            slot = slots[cls._fields.index(key)]
            if slot[1] is not unassigned:
                raise TypeError("Got two values for argument %r" % key)
            slot[1] = value

        return tuple.__new__(cls, (slot[1] for slot in slots))

    def __repr__(self):
        """
        Produce a useful representation of a :class:`RecordInstance`.

            >>> Record('a', 'b', name='Pair')(1, 2)
            Pair(a=1, b=2)
        """
        args = ', '.join('%s=%r' % (field, self[i]) for i, field in enumerate(self._fields))
        return '%s(%s)' % (type(self).__name__, args)

    def _asdict(self):
        """
        Return a dictionary mapping field names to their values.

            >>> Pair = Record('a', 'b', name='Pair')
            >>> r = Pair(1, 2)
            >>> r
            Pair(a=1, b=2)
            >>> r._asdict()
            {'a': 1, 'b': 2}
        """
        return dict(zip(self._fields, self))

    def _replace(self, **kwargs):
        """
        Replace specific fields of this record with new values.

        Because tuples are immutable, this will return a new object.

            >>> Pair = Record('a', 'b', name='Pair')
            >>> r = Pair(1, 2)
            >>> r
            Pair(a=1, b=2)
            >>> r._replace(b=14)
            Pair(a=1, b=14)
        """
        return type(self)(*tuple(kwargs.get(field, self[i]) for i, field in enumerate(self._fields)))


def _get_tests():
    """Enables ``python setup.py test``."""
    import doctest
    return doctest.DocTestSuite(optionflags=doctest.ELLIPSIS)
