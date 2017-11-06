from itertools import product


def probabilities_s_and_t():
    """
    Calculate and print the probability table for p(S, T)
    Therefore the probability p(S) * (p(T|R=1,S=1) + p(T|R=0, S=1)) is calculated.

    :return:
    """
    header = ('S=1, T=1',)
    table = [(_probability_s_and_t(True, True),)]
    _print_table(header, table)


def probabilities_s_under_t():
    """
    Calculate and print the probability table for p(S|T)
    Therefore the probability p(T|S)*p(S)/p(T) is calculated.

    :return:
    """
    header = ('S=1', 'T')
    table = []
    for t in [True, False]:
        prob_s_and_t = _probability_s_and_t(True, t)
        prob_t = 0
        for r in [True, False]:
            prob_t += _probability_rain(r) * _probability_sprinkler(True) * _probability_tracey(t, r, True)
        table.append((round(prob_s_and_t / prob_t, 4), t))
    _print_table(header, table)


def probabilities_s_under_t_and_j():
    """
    Calculate and print the probability table for p(S|T,J)

    :return:
    """
    header = ('S=1', 'T', 'J')
    table = []
    for t, j in product([True, False], [True, False]):
        table.append(('x', t, j))
    _print_table(header, table)


def _probability_rain(r):
    """
    :return: p(R=r)
    """
    if r:
        return 0.2
    return 0.8


def _probability_sprinkler(s):
    """
    :return: p(S=s)
    """
    if s:
        return 0.1
    return 0.9


def _probability_jack(j, r):
    """
    :param r:
    :return: p(J=j|R=r)
    """
    if r:
        prob = 1
    else:
        prob = 0.2
    if j:
        return prob
    return 1 - prob


def _probability_tracey(t, r, s):
    if r and s:
        prob = 1
    elif r and not s:
        prob = 1
    elif not r and s:
        prob = 0.9
    else:
        prob = 0
    if t:
        return prob
    return 1 - prob


def _probability_s_and_t(s, t):
    prob = _probability_sprinkler(s) * (_probability_sprinkler(s) * _probability_tracey(t, True, True) +  _probability_sprinkler(s) * _probability_tracey(t, False, True))
    return prob


def _print_table(header, table):
    print "-" * 10 * len(header)
    row_format = "{:>10}" * len(header)
    print row_format.format(*header)
    print "-" * 10 * len(header)

    for row in table:
        print row_format.format(*row)

    print "-" * 10 * len(header)
    print "\n"

if __name__ == '__main__':
    print 'p(S,T):\n'
    probabilities_s_and_t()

    print 'p(S|T):\n'
    probabilities_s_under_t()

    print 'p(S|T,J):\n'
    probabilities_s_under_t_and_j()