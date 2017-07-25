from collections import Counter, MutableSet, Set, namedtuple
from itertools import combinations, starmap, islice, cycle

from lib import accumulate, rotate, degree_to_index
from describe import describe_object


class PC(object):

    def __init__(self, p):
        self.p = int(p)

    def __int__(self):
        return self.p % 12

    def __sub__(self, other):
        if isinstance(other, IC):
            return PC(int(self) - int(other))
        if isinstance(other, PC):
            return IC(self, other)
        else:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other))
            )

    def __add__(self, other):
        if isinstance(other, IC):
            return PC(int(self) + int(other))
        elif isinstance(other, PC):
            return Cluster([other, self])
        else:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other))
            )

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

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

    @property
    def upper(self):
        return max(self.a, self.b)

    @property
    def lower(self):
        return min(self.a, self.b)

    def __int__(self):
        ab = (self.a - self.b) % 12
        ba = (self.b - self.a) % 12
        return min(ab, ba)

    def __sub__(self, other):
        if isinstance(other, IC):
            return IC(int(self) + int(other))
        else:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other))
            )

    def __add__(self, other):
        if isinstance(other, IC):
            return IC(int(self) + int(other))
        else:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other))
            )

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


class HeptatonicScale(Set):

    Definition = namedtuple(
        "ScaleDefinition",
        ['tonic', 'steps', 'mode']
    )

    def __init__(self, define):
        assert sum(define.steps) == 12
        assert len(define.steps) == 7
        self.define = define

    @property
    def tonic(self):
        return PC(self.define.tonic)

    @property
    def steps(self):
        return map(IC, rotate(self.define.steps, self.define.mode))

    def degree(self, d):
        i = degree_to_index(d)
        note = self.tonic
        for step in xrange(i%7):
            note += self.steps[step%7]
        return note

    def relative_mode(self, d):
        new = self.define._replace(
            tonic=self.degree(d),
            mode=self.define.mode + d - 1
        )
        return HeptatonicScale(new)

    def triad(self, d):
        scale = self.relative_mode(d)
        return Chord([
            scale.degree(1),
            scale.degree(3),
            scale.degree(5)
        ])

    @property
    def key(self):
        return Cluster(self)

    def __len__(self):
        return 7

    def __iter__(self):
        return (self.degree(i) for i in range(1, 8))

    def __contains__(self, o):
        return o in key

    
class Chord(Cluster):

    pass







