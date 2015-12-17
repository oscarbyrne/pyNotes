from notes import Note
from chords import Chord
from scales import Scale

from intervals import __all__
from intervals import *
_g = globals()
for key in Note.keys:
    key_name = key.replace('#', 's')
    _g[key_name] = Note(key)
    __all__.append(key_name)
    for colour in Chord.colours:
        chord_name = key_name + colour.title()
        _g[chord_name] = Chord.from_colour(Note(key), colour)
        __all__.append(chord_name)
    for colour in Scale.colours:
        scale_name = '{}_{}'.format(key_name, colour)
        _g[scale_name] = Scale(key, colour)
        __all__.append(scale_name)
