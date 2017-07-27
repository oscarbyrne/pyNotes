from pitches import PitchClassSet, get_prime_form


class Scale(PitchClassSet):

    def __getitem__(self, degree):
        assert degree > 0
        return self.pitch_classes[(degree-1)%len(self)]

    def interval(self, a, b=1):
        assert a > 0
        assert b > 0
        return self[b] - self[a]

    def triad(self, degree):
        assert degree > 0
        return Chord(self, degree, {1:[0], 3:[0], 5:[0]})

    def parallel_mode(self, n):
        return self.rotated(n).transposed(-self.interval(n+1))

    def relative_mode(self, n):
        return self.transposed(self.interval(n+1))


class Chord(PitchClassSet):

    def __init__(self, scale, degree, voicing):
        self.scale = scale
        self.degree = degree
        self.voicing = voicing

    @property
    def pitches(self):
        pitches = []
        for degree, octaves in self.voicing.items():
            pitch_class = self.scale[degree]
            pitches.extend(pitch_class + (12*octave) for octave in octaves)
        return pitches

    @property
    def prime_form(self):
        return get_prime_form(self.pitches)[0]

    @property
    def rotation(self):
        return get_prime_form(self.pitches)[1]

    @property
    def transposition(self):
        return get_prime_form(self.pitches)[2]

