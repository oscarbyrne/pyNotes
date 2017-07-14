import sys


class MCycle(list):

    def d_to_i(self, d):
        assert 1 <= d
        return (d - 1) % len(self)

    def from_degree(self, d):
        assert 1 <= d <= len(self)
        i = self.d_to_i(d)
        return type(self)(self[i:] + self[:i])

    def __getitem__(self, d):
        if isinstance(d, slice):
            raise SyntaxError("Don't support stepped slice for MCycle")
        else:
            i = self.d_to_i(d)
            return list.__getitem__(self, i)

    def __getslice__(self, start, stop):
        if stop == sys.maxint:
            stop = len(self)
        return [self[i+1] for i in range(start, stop)]



class DiatonicScale(object):

    generators = (
        (2, 2, 1, 2, 2, 2, 1),
        (2, 1, 2, 2, 2, 2, 1)
    )

    modes = {
        "ionian"            : (0, 1),
        "dorian"            : (0, 2),
        "phrygian"          : (0, 3),
        "lydian"            : (0, 4),
        "mixolydian"        : (0, 5),
        "aeolian"           : (0, 6),
        "locrian"           : (0, 7),
        "jazz minor"        : (1, 1),
        "phrygian #6"       : (1, 2),
        "lydian augmented"  : (1, 3),
        "overtone scale"    : (1, 4),
        "mixolydian b6"     : (1, 5),
        "locrian #2"        : (1, 6),
        "altered scale"     : (1, 7)
    }

    @classmethod
    def from_name(cls, tonic, name):
        return cls.from_define(tonic, *cls.modes[name])

    @classmethod
    def from_define(cls, tonic, gen, mode):
        return cls(tonic, cls.generators[gen], mode)

    def __init__(self, tonic, steps, mode=1):
        self.tonic = tonic
        self.steps = MCycle(steps).from_degree(mode)

    def parallel_mode(self, *define):
        if isinstance(define[0], basestring):
            return type(self).from_name(self.tonic, define[0])
        else:
            return type(self).from_define(self.tonic, *define)
        
    def relative_mode(self, degree):
        return type(self)(self.note(degree), self.steps)

    def degrees(self):
        return xrange(1, len(self.steps) + 1)

    def interval(self, d2, d1=1):
        assert 1 <= d1
        assert 1 <= d2
        d1, d2 = sorted([d1-1, d2-1])
        return sum(self.steps[d1:d2])

    def intervals(self):
        return [self.interval(d) for d in self.degrees()]

    def note(self, d):
        assert 1 <= d
        return self.tonic + self.interval(d)

    def notes(self):
        return [self.note(d) for d in self.degrees()]

    def triad(self, d):
        assert 1 <= d
        return Chord.triad(self, d)

    def __getitem__(self, d):
        return self.triad(d)



class Chord(object):

    @classmethod
    def triad(cls, scale, degree):
        assert 1 <= degree <= 7
        return cls(scale.relative_mode(degree), [1, 3, 5])

    def __init__(self, scale, degrees):
        self.scale = scale
        self.degrees = set(degrees)

    def add(self, d):
        assert 1<= d <= 13
        self.degrees.add(d)
        return self

    def no(self, d):
        assert 1<= d <= 13
        self.degrees.remove(d)
        return self

    def sus(self, d):
        assert d in [2, 4]
        return self.no(3).add(d)

    def transpose(self, n):
        self.scale.tonic += n
        return self

    def notes(self):
        return [self.scale.note(d) for d in self.degrees]

    def intervals(self):
        return [self.scale.interval(d) for d in self.degrees]


