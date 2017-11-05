def probabilities_s_and_t():
    _print_table(('a', 'b', 'c'), [(1, 2, 3), (4, 5, 6)])


def probabilities_s_under_t():
    pass


def probabilities_s_under_t_and_j():
    pass


def _print_table(header, table, spaces=1):
    line = ''
    for col in header:
        line += '\t' * spaces
        line += str(col)
    print line
    for row in table:
        line = ''
        for col in row:
            line += '\t' * spaces
            line += str(col)
        print line
    print '\n'


if __name__ == '__main__':
    print 'p(S,T):\n'
    probabilities_s_and_t()

    print 'p(S|T):\n'
    probabilities_s_under_t()

    print 'p(S|T,J):\n'
    probabilities_s_under_t_and_j()