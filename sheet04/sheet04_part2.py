cpd = {
    frozenset({'x1': True}.items()): 0.05,
    frozenset({'x1': False}.items()): 4.95,
    frozenset({'x2': True}.items()): 2.5,
    frozenset({'x2': False}.items()): 2.5,
    frozenset({'x3': True, 'x1': True}.items()): 0.25,
    frozenset({'x3': False, 'x1': True}.items()): 4.75,
    frozenset({'x3': True, 'x1': False}.items()): 0.05,
    frozenset({'x3': False, 'x1': False}.items()): 4.95,
    frozenset({'x4': True, 'x2': True}.items()): 0.5,
    frozenset({'x4': False, 'x2': True}.items()): 4.5,
    frozenset({'x4': True, 'x2': False}.items()): 0.05,
    frozenset({'x4': False, 'x2': False}.items()): 4.95,
    frozenset({'x5': True, 'x2': True}.items()): 3.,
    frozenset({'x5': False, 'x2': True}.items()): 2.,
    frozenset({'x5': True, 'x2': False}.items()): 1.5,
    frozenset({'x5': False, 'x2': False}.items()): 3.5,
    frozenset({'x6': True, 'x8': True}.items()): 4.9,
    frozenset({'x6': False, 'x8': True}.items()): 0.1,
    frozenset({'x6': True, 'x8': False}.items()): 0.25,
    frozenset({'x6': False, 'x8': False}.items()): 4.75,
    frozenset({'x8': True, 'x4': True, 'x3': True}.items()): 5.,
    frozenset({'x8': False, 'x4': True, 'x3': True}.items()): 0.,
    frozenset({'x8': True, 'x4': False, 'x3': True}.items()): 5.,
    frozenset({'x8': False, 'x4': False, 'x3': True}.items()): 0.,
    frozenset({'x8': True, 'x4': True, 'x3': False}.items()): 5.,
    frozenset({'x8': False, 'x4': True, 'x3': False}.items()): 0.,
    frozenset({'x8': True, 'x4': False, 'x3': False}.items()): 5.,
    frozenset({'x8': False, 'x4': False, 'x3': False}.items()): 0.,
    frozenset({'x7': True, 'x5': True, 'x8': True}.items()): 4.5,
    frozenset({'x7': False, 'x5': True, 'x8': True}.items()): 0.5,
    frozenset({'x7': True, 'x5': False, 'x8': True}.items()): 3.5,
    frozenset({'x7': False, 'x5': False, 'x8': True}.items()): 1.5,
    frozenset({'x7': True, 'x5': True, 'x8': False}.items()): 4.,
    frozenset({'x7': False, 'x5': True, 'x8': False}.items()): 1.,
    frozenset({'x7': True, 'x5': False, 'x8': False}.items()): 0.5,
    frozenset({'x7': False, 'x5': False, 'x8': False}.items()): 4.5,
}


def h(query):
    return frozenset(query.items())


if __name__ == '__main__':
