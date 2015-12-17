from common import NoteCluster
from notes import Note
from intervals import *
from intervals import Interval


class Chord(NoteCluster):

    colours = {
        "maj" :  (P1, M3, P5),
        "min" :  (P1, m3, P5),
        "dim" :  (P1, m3, d5),
        "aug" :  (P1, M3, A5),
        "maj7" : (P1, M3, P5, M7),
        "min7" : (P1, m3, P5, m7),
    }

    @classmethod
    def from_intervals(cls, root, intervals, **kwargs):
        return cls(root, sorted(intervals), **kwargs)

    @classmethod
    def from_notes(cls, root, notes, **kwargs):
        return cls(root, [Note(root) - Note(note) for note in notes], **kwargs)

    @classmethod
    def from_colour(cls, root, colour, **kwargs):
        return cls(root, list(cls.colours[colour.lower()]), **kwargs)

    def __init__(self, root, intervals, inversion=0):
        self.root = Note(root)
        self.intervals = intervals
        self.inversion = inversion

    @property
    def colour(self):
        for name, intervals in Chord.colours.iteritems():
            if self.intervals == list(intervals):
                return name
        else:
            return "unknown"

    @property
    def name(self):
        return str(self.root).replace('#', 's') + self.colour.title()

    def inverted(self, i):
        return Chord.from_intervals(self.root, self.intervals, inversion=i)

    @property
    def inversion(self):
        return self._inversion

    @inversion.setter
    def inversion(self, i):
        assert i < len(self), "inversion number too high"
        self._inversion = i

    @property
    def notes(self):
        notes = [self.root + n for n in self.intervals]
        for note in notes[:self.inversion]:
            note += 12
        return sorted(notes)

    def add_note(self, note):
        return Chord.from_notes(
            self.root,
            [note] + self.notes
        )

    def remove_note(self, note):
        return Chord.from_notes(
            self.root,
            [n for n in self.notes if n != note]
        )

    def add_interval(self, interval):
        return Chord.from_intervals(
            self.root,
            [interval] + self.intervals
        )

    def remove_interval(self, interval):
        return Chord.from_intervals(
            self.root,
            [i for i in self.intervals if i != interval]
        )

    def __add__(self, value):
        strategy = {
            Interval :  self.add_interval,
            Note :      self.add_note,
        }[type(value)]
        return strategy(value)

    def __sub__(self, value):
        strategy = {
            Interval :  self.remove_interval,
            Note :      self.remove_note,
        }[type(value)]
        return strategy(value)

    def __len__(self):
        return len(self.intervals)

    def __repr__(self):
        return "{}: {}".format(self.name, NoteCluster.__repr__(self))
