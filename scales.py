from common import NoteCluster
from notes import Note
from chords import Chord
from intervals import *


class Scale(NoteCluster):

    colours = {
        "major": [P1, M2, M3, P4, P5, M6, M7],
        "minor": [P1, M2, m3, P4, P5, m6, m7],
    }

    def __init__(self, root, colour="major"):
        self.root = Note(root)
        self.intervals = Scale.colours[colour.lower()]

    def __len__(self):
        return len(self.intervals)

    def __getitem__(self, i):
        octaves, degree = divmod(i, len(self))
        return self.root + (octaves*12) + self.intervals[degree]

    @property
    def notes(self):
        return [self[i] for i in xrange(len(self))]

    @property
    def triads(self):
        return [Chord.from_notes(root, [root, self[i+2], self[i+4]]) for i, root in enumerate(self.notes)]

    def __str__(self):
        marks = [" "] * 36
        for degree, note in enumerate(self.notes):
            marks[note.i] = str((degree + 1)%8)
        return NoteCluster.keyboard + " ".join(marks)
