from abc import ABCMeta, abstractproperty

from notes import Note


class NoteCluster(object):

    __metaclass__ = ABCMeta

    keyboard = (
        "  #   #     #   #   #     #   #     #   #   #     #   #     #   #   #   \n"
        "  #   #     #   #   #     #   #     #   #   #     #   #     #   #   #   \n"
        "  |   |     |   |   |     |   |     |   |   |     |   |     |   |   |   \n"
        "c | d | e f | g | a | b c | d | e f | g | a | b c | d | e f | g | a | b \n"
    )

    def __init__(self, notes):
        self.notes = notes

    def __str__(self):
        marks = [" "] * 36
        for note in self.notes:
            marks[note.i] = "x"
        return NoteCluster.keyboard + " ".join(marks)

    def __repr__(self):
        return "{" + ", ".join(repr(note) for note in self.notes) + "}"

    def __contains__(self, value):
        if isinstance(value, NoteCluster):
            return all(note in self for note in value.notes)
        elif isinstance(value, Note):
            return value.i%12 in [note.i%12 for note in self.notes]
        else:
            raise SyntaxError()
    # 
    # def __eq__(self, other):
    #     if isinstance(value, NoteCluster):
    #         for
