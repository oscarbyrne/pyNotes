A command-line composers tool for exploring diatonic music via musical set theory.

By defining groups of notes by their 'prime form' (see: http://composertools.com/Theory/PCSets/PCSets3.htm), we can efficiently classify them and list related musical objects.

## Usage:
    python -i sample.py
    >>> maj_chord = PitchClassSet.from_pitches([0,4,7])
    >>> maj_chord.name
    'Major Chord'
    >>> print maj_chord.similar_sets
    >>> print maj_chord.supersets
    >>> jazz_minor = maj_chord.super_sets[14]
    >>> jazz_minor = Scale.from_pitches(jazz_minor.pitch_classes)
    >>> jazz_minor.relative_mode(2)
    >>> jazz_minor.triad(2)
  
