class Pitch(object):

    def __init__(self, other):
        if isinstance(other, Pitch):
            self.p = other.p
        else:
            self.p = other

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = int(value)

    def transposed(self, i):
        return type(self)(self.p + i)

    def inverted(self, plane=0):
        raise NotImplementedError("todo")

    def __int__(self):
        return self.p

    def __cmp__(self, other):
        return cmp(int(self), int(other))

    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            self.p
        )


class PitchClass(Pitch):

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = int(value) % 12


def IntervalClass(a, b):
    """
    See: https://en.wikipedia.org/wiki/Interval_class
    """
    ab = (int(a) - int(b)) % 12
    ba = (int(b) - int(a)) % 12
    return min(ab, ba)
