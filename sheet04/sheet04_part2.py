from itertools import product


def brute_force():
    for var in ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']:
        variables = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']
        variables.remove(var)

        factorsum_true = 0
        factorsum_false = 0
        for x in product(*[[True, False]] * 7):
            parameters = {k: v for k, v in zip(variables, x)}
            parameters[var] = True
            factorsum_true += phi(**parameters)
            parameters[var] = False
            factorsum_false += phi(**parameters)

        print('phi({}) = \t{:>10},\t{:>10}'.format(var, round(factorsum_true, 2), round(factorsum_false, 2)))


def phi(x1, x2, x3, x4, x5, x6, x7, x8):
    return phi_x1(x1) * phi_x2(x2) * _phi_x3_x1(x3, x1) * _phi_x4_x2(x4, x2) * _phi_x5_x2(x5, x2) * _phi_x6_x8(x6, x8) * _phi_x7_x5_x8(x7, x5, x8) * _phi_x8_x4_x3(x8, x4, x3)


def phi_x1(x1):
    return 0.05 if x1 else 4.95


def phi_x2(x2):
    return 2.5


def _phi_x3_x1(x3, x1):
    if x1:
        return 0.25 if x3 else 4.75
    else:
        return 0.05 if x3 else 4.95


def _phi_x4_x2(x4, x2):
    if x2:
        return 0.5 if x4 else 4.5
    else:
        return 0.05 if x4 else 4.95


def _phi_x5_x2(x5, x2):
    if x2:
        return 3 if x5 else 2
    else:
        return 1.5 if x5 else 3.5


def _phi_x6_x8(x6, x8):
    if x8:
        return 4.9 if x6 else 0.1
    else:
        return 0.25 if x6 else 4.75


def _phi_x8_x4_x3(x8, x4, x3):
    if not x4 and not x3:
        return 0 if x8 else 5
    else:
        return 5 if x8 else 0


def _phi_x7_x5_x8(x7, x5, x8):
    if x5 and x8:
        return 4.5 if x7 else 0.5
    if not x5 and x8:
        return 3.5 if x7 else 1.5
    if x5 and not x8:
        return 4 if x7 else 1
    if not x5 and not x8:
        return 0.5 if x7 else 4.5


if __name__ == '__main__':
    brute_force()
