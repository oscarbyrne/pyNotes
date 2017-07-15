from functools import wraps
import sys

this = sys.modules[__name__]

this.VERBOSITY=5

def set_verbosity(v):
    assert v in range(6)
    print "New verbosity: {} (default is 5)".format(v)
    this.VERBOSITY = v


keyboard = {
    "keys" : (
        "|  | | | |  |  | | | | | |  | \n"
        "|  | | | |  |  | | | | | |  | \n"
        "|  | | | |  |  | | | | | |  | \n"
        "|  |_| |_|  |  |_| |_| |_|  | \n"
        "|   |   |   |   |   |   |   | \n"
        "|   |   |   |   |   |   |   | \n"
        "|___|___|___|___|___|___|___| \n"
    ),
    "indices" : [
        2, 4, 6, 8, 10, 14, 16, 18, 20, 22, 24, 26
    ]
}


names = {
    "PC" : (
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B"
    ),

    "IC" : (
        "unison",
        "m2 / M7",
        "M2 / m7",
        "m3 / M6",
        "M3 / m6",
        "P4 / P5",
        "tritone"
    )
}


def printer(func):
    @wraps(func)
    def verbose_sensitive(*args, **kwargs):
        if kwargs.pop("LEVEL") <= VERBOSITY:
            return func(*args) + "\n"
        else:
            return ""
    return verbose_sensitive

@printer
def print_heading(title, size):
    assert size in range(4)
    underline = ["=", "~", "-", " "][size]
    return (
        "{} \n"
        "{}"
    ).format(
        title.title(),
        underline * len(title)
    )

@printer
def print_line(line):
    return line

@printer
def print_on_keyboard(pitches):
    tone_row = [" "] * 28
    for pc in pitches:
        tone_row[keyboard["indices"][int(pc)]] = "X"
    return keyboard["keys"] + "".join(tone_row)

@printer
def print_interval_vector(cluster):
    count = [0]*7
    for i, c in cluster.interval_vector.items():
        count[int(i)] = c
    return "<{1},{2},{3},{4},{5},{6}>".format(*count)


def describe_pitch(pitch):
    p = int(pitch)
    outstring  = print_heading("Pitch Class {}".format(p), 0            , LEVEL=1)
    outstring += print_line(""                                          , LEVEL=3)
    outstring += print_line(names["PC"][p]                              , LEVEL=0)
    outstring += print_line(""                                          , LEVEL=3)
    outstring += print_on_keyboard([p]                                  , LEVEL=3)
    return outstring

def describe_interval(interval):
    i = int(interval)
    outstring  = print_heading("Interval Class {}".format(i), 0         , LEVEL=1)
    outstring += print_line(""                                          , LEVEL=3)
    outstring += print_line(names["IC"][i]                              , LEVEL=0)
    outstring += print_line(""                                          , LEVEL=3)
    outstring += print_on_keyboard([interval.a, interval.b]             , LEVEL=3)
    return outstring

def describe_cluster(cluster):
    outstring  = print_heading("Tone Cluster", 0                        , LEVEL=1)
    outstring += print_interval_vector(cluster                          , LEVEL=0)
    outstring += print_line(""                                          , LEVEL=3)
    outstring += print_on_keyboard(cluster                              , LEVEL=3)
    return outstring



def describe_object(obj):
    descrition = {
        "PC" :      describe_pitch,
        "IC" :      describe_interval,
        "Cluster" : describe_cluster,
    }[type(obj).__name__]
    return "\n" + descrition(obj) + "\n"
