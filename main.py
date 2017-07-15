from collections import Sequence
from itertools import combinations, chain


class Cycle(Sequence):

    def __init__(self, sequence):
        self.items = list(sequence)

    def rotate(self, i):
        return Cycle(self.items[i:] + self.items[:i])

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return islice(self, i.start, i.stop, i.step)
        else:
            return self.items[i % len(self)]

    def __repr__(self):
        return "Cycle({})".format(repr(self.items))


class PC(object):

    names = (
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B"
    )

    def __init__(self, p):
        self.p = int(p)

    @property
    def name(self):
        return PC.names[int(self)]

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
        return "Pitch {} ({})".format(
            int(self),
            self.name
        )

    def __repr__(self):
        return "PC({})".format(int(self))


class IC(object):

    names = (
        "unison",
        "m2 / M7",
        "M2 / m7",
        "m3 / M6",
        "M3 / m6",
        "P4 / P5",
        "tritone"
    )

    def __init__(self, a, b=0):
        self.a = int(a)
        self.b = int(b)

    @property
    def name(self):
        return IC.names[int(self)]

    def __int__(self):
        ab = (self.a - self.b) % 12
        ba = (self.b - self.a) % 12
        return min(ab, ba)

    def __str__(self):
        return "Interval {} ({})".format(
            int(self),
            self.name
        )

    def __repr__(self):
        return "IC({})".format(int(self))


class Vector(object):

    def __init__(self, pitch_set):
        self.pitch_set = pitch_set

    @property
    def pairs(self):
        return combinations(self.pitch_set, 2)

    @property
    def count(self):
        counter = [0] * 7
        for a, b in self.pairs:
            i = IC(a, b)
            counter[int(i)] += 1
        return counter

    def __str__(self):
        def format_interval(i):
            return "{}  * {}".format(
                self.count[i],
                IC.names[i]
            )
        return (
            "                  \n" +
            "Interval vector   \n" +
            "----------------- \n" +
            "{}                \n" +
            "                  \n" +
            "Pitch Classes:    \n" +
            "                  \n" +
            "  {}              \n" +
            "                  \n" +
            "Interval Classes: \n" +
            "                  \n" +
            "  {}              \n" * 6
        ).format(
            repr(self),
            "\n  ".join(str(p) for p in self.pitch_set),
            *(format_interval(i) for i in range(1, 7))
        )

    def __repr__(self):
        return "< {1} {2} {3} {4} {5} {6} >".format(*self.count)


class Cluster(object):

    def __init__(self, ps):
        self.pitch_set = set()
        for p in ps:
            self.add(p)

    @property
    def interval_vector(self):
        return Vector(self)
        
    def add(self, p):
        p = PC(p)
        self.pitch_set.add(p)
        return self

    def __iter__(self):
        notes = list(self.pitch_set)
        return iter(sorted(notes))

    def __add__(self, p):
        new = Cluster(self)
        return new.add(p)

    def __str__(self):
        return str(self.interval_vector)

    def __repr__(self):
        return "Cluster([{}])".format(
            ", ".join(repr(p) for p in self)
        )


