class Note(object):

    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    @classmethod
    def name_to_index(cls, name):
        key = name[0].upper()
        intonation = name[1:].count('#') - name[1:].count('b')
        return Note.keys.index(key) + intonation

    def __init__(self, value):
        if type(value) is int:
            self.i = value
        elif type(value) is Note:
            self.i = value.i
        else:
            self.i = Note.name_to_index(value)

    def __iadd__(self, n):
        self.i += n

    def __add__(self, n):
        return Note(self.i + n)

    def __sub__(self, n):
        if type(n) is Note:
            return abs(self.i - n.i)
        else:
            return Note(self.i - n)

    def __cmp__(self, other):
        if type(other) is Note:
            return int.__cmp__(self.i, other.i)
        else:
            raise SyntaxError("Cannot compare Note and {}".format(type(other)))

    def __str__(self):
        return Note.keys[self.i%12]

    def __repr__(self):
        return "{}{}".format(self, self.i // 12)
