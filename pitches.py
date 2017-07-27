from collections import Set
from copy import copy


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
    prime_form = [pitch - transposition for pitch in normal_form]
    return prime_form, rotation, transposition


class PitchClassSet(Set):

    @classmethod
    def from_pitches(cls, pitches):
        return cls(*get_prime_form(pitches))

    def __init__(self, prime_form, rotation, transposition):
        self.prime_form = prime_form
        self.rotation = rotation
        self.transposition = transposition

    def __contains__(self, other):
        return other in self.pitches

    def __iter__(self, other):
        return iter(self.pitches)

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

    def transposed(self, i):
        return type(self)(self.prime_form, self.rotation, self.transposition - i)

    def rotated(self, n):
        return type(self)(self.prime_form, self.rotation - n, self.transposition)

    def supersets(self):
        raise NotImplementedError("todo")

    def subsets(self):
        raise NotImplementedError("todo")

    def related_sets(self):
        raise NotImplementedError("todo")

    def __repr__(self):
        return "{}({},{},{})".format(
            type(self).__name__,
            self.prime_form,
            self.rotation,
            self.transposition
        )

    def __str__(self):
        raise NotImplementedError("todo")
