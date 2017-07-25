from itertools import cycle, islice


def accumulate(iterable):
    total = 0
    for x in iterable:
        total += x
        yield total

def rotate(iterable, n):
    return islice(cycle(iterable), n, n+len(iterable))


def index_to_degree(i):
    if i < 0:
        return i - 1
    else:
        return i + 1

def degree_to_index(d):
    if d < 0:
        return d + 1
    elif d > 0:
        return d - 1
    else:
        raise SyntaxError("No such thing as zeroth degree!")