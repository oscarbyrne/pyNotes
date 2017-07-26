from collections import MutableSet

from pitch_sets import OrderedPitchSet, UnorderedPitchSet


class DiatonicScale(OrderedPitchSet):

    def __init__(self):
        raise NotImplementedError("todo")


class Chord(UnorderedPitchSet, MutableSet):

    def __init__(self):
        raise NotImplementedError("todo")
