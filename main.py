from collections import Sequence, namedtuple
from itertools import islice, combinations


class Cycle(Sequence):

    def __init__(self, iterable):
        self.items = list(iterable)

    def rotate(self, i):
        return type(self)(self.items[i:] + self.items[:i])

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return islice(self, i.start, i.stop, i.step)
        else:
            return self.items[i % len(self)]

    def __repr__(self):
        return "Cycle({})".format(repr(self.items))


class Pitch(object):

    def __init__(self, p):
        self.p = p

    @property
    def pitch_class(self):
        return self.p%12

    def __add__(self, p):
        return Pitch(self.p + p)

    def __sub__(self, p):
        return Pitch(self.p - p)

    def __rshift__(self, other):
        return Interval(other.p - self.p)

    def __str__(self):
        return str(self.pitch_class)


class Interval(object):

    names = (
        "unison",
        "m2 / M7",
        "M2 / m7",
        "m3 / M6",
        "M3 / m6",
        "P4 / P5",
        "tritone"
    )

    def __init__(self, pitch_interval):
        self.ip = abs(pitch_interval)

    @property
    def interval_class(self):
        ip1 =  abs(0 - self.ip%12)
        ip2 = abs(12 - self.ip%12)
        return min(ip1, ip2)

    def __str__(self):
        return type(self).names[self.interval_class]


class IntervalVector(object):

    def __init__(self, pitch_set):
        self.counter = [0] * 7
        pairs = combinations(pitch_set, 2)
        for a,b in pairs:
            i = (a >> b).interval_class
            self.counter[i] += 1

    def __str__(self):
        return "< {1} {2} {3} {4} {5} {6} >".format(*self.counter)


class DiatonicScale(object):

    Definition = namedtuple(
        "ScaleDefinition",
        ['tonic', 'gen', 'rot']
    )

    generators = (
        (2, 2, 1, 2, 2, 2, 1),
        (2, 1, 2, 2, 2, 2, 1)
    )

    names = (
        (
            "ionian",
            "dorian",
            "phrygian",
            "lydian",
            "mixolydian",
            "aeolian",
            "locrian"
        ),
        (
            "jazz minor",
            "phrygian #6",
            "lydian augmented",
            "overtone scale",
            "mixolydian b6",
            "locrian #2",
            "altered scale"
        )
    )

    def __init__(self, tonic, generator, rotation):
        self.define = type(self).Definition(tonic, generator, rotation)

    def relative_mode(self, d):
        tonic, gen, rot = self.define
        return type(self)(self.note(d), gen, rot + d)

    @property
    def tonic(self):
        return Pitch(self.define.tonic)

    @property
    def mode(self):
        return Cycle(type(self).names[self.define.gen])[self.define.rot]

    @property
    def generator(self):
        return Cycle(type(self).generators[self.define.gen])

    @property
    def steps(self):
        return self.generator.rotate(self.define.rot)

    def note(self, d):
        assert d > 0
        return self.tonic + sum(self.generator[:d-1])

    @property
    def degrees(self):
        return xrange(1, 8)

    @property
    def pitch_set(self):
        return [self.note(d) for d in self.degrees]

    def interval(self, d2, d1=1):
        return self.note(d1) >> self.note(d2)

    @property
    def intervals(self):
        return [self.interval(d) for d in self.degrees]

    @property
    def interval_vector(self):
        return IntervalVector(self.pitch_set)

    def __getitem__(self, d):
        assert d > 0
        return Chord.triad(self, d)

    def __str__(self):
        return (
            "                             \n"
            "    Scale:       {} {}       \n"
            "    ------                   \n"
            "    Pitches:     {}          \n"
            "    Intervals:   {}          \n"
        ).format(
            self.tonic,
            self.mode,
            [str(n) for n in self.pitch_set],
            self.interval_vector
        )
