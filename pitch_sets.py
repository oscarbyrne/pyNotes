from collections import Iterable, Sequence, Set, Counter
from sys import maxint
from operator import methodcaller
from itertools import combinations, starmap

from pitches import Pitch, IntervalClass


class PitchCollection(Iterable):

    def to_simple_form(self):
        return type(self.pitches)(map(int, self.pitches))

    def __init__(self, pitches):
        self.pitches = map(Pitch, pitches)

    def __iter__(self):
        return iter(self.pitches)

    def transposed(self, i):
        return type(self)(
            pitch.transposed(i) for pitch in self
        )

    def inverted(self, plane=0):
        return type(self)(
            pitch.inverted(plane) for pitch in self
        )

    @property
    def interval_vector(self):
        pairs = combinations(self, 2)
        return Counter(starmap(IntervalClass, pairs))

    @property
    def prime_form(self):
        """
        From Rahn algorithm
        See: http://composertools.com/Theory/PCSets/PCSets3.htm
        """
        pcs = OrderedPitchSet(self.pitches).sorted()        # sort pitches
        rot = [pcs.rotated(i) for i in xrange(len(self))]   # all possible rotations
        seq = [-1] + range(1, len(self) - 1)                # most emphasis on distance from first to last
        for i in reversed(seq):                             # exploiting python's stable sorting
            rot = sorted(
                rot,
                key=methodcaller('interval', 0, i)
            )
        norm = rot[0]
        return norm.zeroed()

    def __repr__(self):
        return "{}([{}])".format(
            type(self).__name__,
            ",".join(str(pitch) for pitch in self)
        )


class OrderedPitchSet(PitchCollection, Sequence):

    @property
    def pitches(self):
        return self._pitches

    @pitches.setter
    def pitches(self, value):
        self._pitches = list(value)

    def __getitem__(self, given):
        return self.pitches[given % len(self)]

    def __getslice__(self, start, stop):
        if stop == maxint:
            stop = len(self)
        return type(self)(
            self[i] for i in range(start, stop)
        )

    def __add__(self, other):
        return type(self)(
            self.pitches + other.pitches
        )

    def __len__(self):
        return len(self.pitches)

    def sorted(self, key=None, reverse=False):
        return type(self)(
            sorted(self.pitches, key=key, reverse=reverse)
        )

    def rotated(self, n):
        """
        Equivalent to chord inversion
        """
        assert len(self) >= n
        return type(self)(
            self[n:] + self[:n].transposed(12)
        )

    def zeroed(self):
        return self.transposed(-int(self[0]))

    def interval(self, i, j):
        return int(self[j]) - int(self[i])


class UnorderedPitchSet(PitchCollection, Set):

    @property
    def pitches(self):
        return self._pitches

    @pitches.setter
    def pitches(self, value):
        self._pitches = set(value)

    def __contains__(self, pitch):
        return pitch in self.pitches

    def __len__(self):
        return len(self.pitches)

