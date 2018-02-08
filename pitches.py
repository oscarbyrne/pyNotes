from collections import Set, Counter, Sequence
from copy import copy
from itertools import combinations, starmap

from names import prime_forms, duodecimal


def IntervalClass(a, b):
    """
    See: https://en.wikipedia.org/wiki/Interval_class
    """
    ab = (int(a) - int(b)) % 12
    ba = (int(b) - int(a)) % 12
    return min(ab, ba)


def PitchClass(p):
    return p % 12


def get_prime_form(pitches):
    """
    From Rahn algorithm
    See: http://composertools.com/Theory/PCSets/PCSets3.htm
    - sort pitches
    - find all possible rotations
    - rank these minimising jumps (exploit python's stable sorting here)
    - scale to root pitch
    """
    pitches = sorted(set(pitches))
    cardinality = len(pitches)
    rotate = lambda pitches, n: pitches[n:] + [p+12 for p in pitches[:n]]
    rotations = [rotate(pitches, n) for n in range(cardinality)]
    distances = [-1] + range(1, cardinality - 1)
    candidates = copy(rotations)
    for i in reversed(distances):
        candidates = sorted(
            candidates,
            key=lambda c: c[i] - c[0]
        )
    normal_form = candidates[0]
    rotation = rotations.index(normal_form)
    transposition = normal_form[0]
    prime_form = tuple(pitch - transposition for pitch in normal_form)
    return prime_form, rotation, transposition


class PitchClassSetContainer(Sequence):

    def __init__(self, pc_sets):
        self.pc_sets = pc_sets

    def __getitem__(self, i):
        return self.pc_sets[i]

    def __len__(self):
        return len(self.pc_sets)

    def __repr__(self):
        return repr(self.pc_sets)

    def __str__(self):
        s = "\n"
        for i, p in enumerate(self.pc_sets):
            s += "{} {}\n".format(
                "[{}]".format(i).ljust(6),
                str(p)
            )
        return s
        


class PitchClassSet(Set):
    # TO DO: This should be a sequence!

    @classmethod
    def from_pitches(cls, pitches):
        if isinstance(pitches, basestring):
            pitches = [duodecimal.index(c) for c in pitches]
        return cls(*get_prime_form(pitches))

    def __init__(self, prime_form, rotation, transposition):
        self.prime_form = tuple(prime_form)
        self.rotation = rotation
        self.transposition = transposition

    def __contains__(self, other):
        return other in self.pitch_classes

    def __iter__(self):
        return iter(self.pitch_classes)

    def __len__(self):
        return len(self.prime_form)

    @property
    def normal_form(self):
        return [PitchClass(interval + self.transposition) for interval in self.prime_form]

    @property
    def pitch_classes(self):
        return self.normal_form[-self.rotation:] + self.normal_form[:-self.rotation]

    @property
    def interval_vector(self):
        pairs = combinations(self, 2)
        return Counter(starmap(IntervalClass, pairs))

    @property
    def supersets(self):
        supersets = []
        for prime_form in [pf for pf in prime_forms if len(pf) > len(self)]:
            for i in range(12):
                c = PitchClassSet(prime_form, 0, i)
                if set(self.pitch_classes).issubset(c.pitch_classes):
                    supersets.append(c)
        return PitchClassSetContainer(supersets)

    @property
    def subsets(self):
        subsets = []
        for r in range(1, len(self)):
            c = combinations(self, r)
            subsets.extend(map(PitchClassSet.from_pitches, c))
        return PitchClassSetContainer(subsets)

    @property
    def similar_sets(self):
        """
        Return pitch sets (of same length) which differ by one pitch
        See: http://composertools.com/Theory/PCSets/PCSets9.htm
        """
        similar = []
        for i in range(len(self)):
            c = [p for p in range(12) if p not in self]
            s = [self.pitch_classes] * len(c)
            for j, p in enumerate(s):
                p[i] = c[j]
                s[j] = PitchClassSet.from_pitches(p)
            similar.extend(s)
        return PitchClassSetContainer(similar)

    @property
    def name(self):
        try:
            return prime_forms[self.prime_form]
        except KeyError:
            return "Unnamed set"

    def transposed(self, i):
        return type(self)(self.prime_form, self.rotation, self.transposition + i)

    def rotated(self, n):
        return type(self)(self.prime_form, self.rotation - n, self.transposition)

    def __repr__(self):
        return "{}({},{},{})".format(
            type(self).__name__,
            self.prime_form,
            self.rotation,
            self.transposition
        )

    def __str__(self):
        pitches = "".join(duodecimal[pc] for pc in self.pitch_classes)
        intervals = ["0"]*6
        for k, v in self.interval_vector.items():
            intervals[k-1] = duodecimal[v]
        return "{} <{}> : {}".format(
            pitches.ljust(12),
            "".join(intervals),
            self.name
        )
