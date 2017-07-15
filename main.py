from collections import Counter, MutableSet
from itertools import combinations, starmap

from describe import describe_object, set_verbosity


class PC(object):

    def __init__(self, p):
        self.p = int(p)

    def __int__(self):
        return self.p % 12

    def __sub__(self, other):
        return IC(self, other)

    def __add__(self, other):
        try:
            return Cluster(other) + self
        except TypeError:
            return Cluster([other, self])

    def __cmp__(self, other):
        return cmp(int(self), int(other))

    def __hash__(self):
        return hash(int(self))

    def __str__(self):
        return describe_object(self)

    def __repr__(self):
        return "PC({})".format(int(self))


class IC(object):

    def __init__(self, a, b=0):
        self.a = int(a)
        self.b = int(b)

    def __int__(self):
        ab = (self.a - self.b) % 12
        ba = (self.b - self.a) % 12
        return min(ab, ba)

    def __cmp__(self, other):
        return cmp(int(self), int(other))

    def __hash__(self):
        return hash(int(self))

    def __str__(self):
        return describe_object(self)

    def __repr__(self):
        return "IC({})".format(int(self))


class Cluster(MutableSet):

    def __init__(self, ps):
        self.pitch_set = set()
        for p in ps:
            self.add(p)

    @property
    def interval_vector(self):
        pairs = combinations(self, 2)
        return Counter(starmap(IC, pairs))
        
    def add(self, p):
        p = PC(p)
        self.pitch_set.add(p)
        return self

    def discard(self, p):
        p = PC(p)
        self.pitch_set.discard(p)
        return self

    def __contains__(self, p):
        p = PC(p)
        return p in self.pitch_set

    def __len__(self):
        return len(self.pitch_set)

    def __iter__(self):
        notes = list(self.pitch_set)
        return iter(sorted(notes))

    def __add__(self, p):
        new = Cluster(self)
        return new.add(p)

    def __str__(self):
        return describe_object(self)

    def __repr__(self):
        return "Cluster([{}])".format(
            ", ".join(repr(p) for p in self)
        )




