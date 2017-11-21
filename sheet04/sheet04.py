
class Factor(object):
    def __init__(self, scope, cpd):
        self.scope = set(scope)
        self.cpd = cpd

    def _get_values_from_cpd(self):


    def __str__(self):
        elements = ', '.join(self.scope)
        return 'phi({})'.format(elements)

    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        assert(isinstance(other, Factor))

        new_scope = set(self.scope).union(other.scope)
        return Factor(new_scope, self.cpd)

    def sum_out(self, variable):
        self.scope.remove(variable)

    def values(self, variable):
        pass


def eliminate_var(factors, variable):
    factors1 = [phi for phi in factors if variable in phi.scope]
    factors2 = [phi for phi in factors if variable not in phi.scope]

    psi = factors1[0]
    for phi in factors1[1:]:
        psi *= phi

    psi.sum_out(variable)
    factors2.append(psi)
    return factors2


def variable_elimination(factors, variables):
    for var in variables:
        factors = eliminate_var(factors, var)

    result = factors[0]
    for phi in factors[1:]:
        result *= phi

    return result


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
    phi_1 = Factor({'x1'}, cpd)
    phi_13 = Factor({'x1', 'x3'}, cpd)
    phi_2 = Factor({'x2'}, cpd)
    phi_24 = Factor({'x2', 'x4'}, cpd)
    phi_25 = Factor({'x2', 'x5'}, cpd)
    phi_68 = Factor({'x6', 'x8'}, cpd)
    phi_348 = Factor({'x3', 'x4', 'x8'}, cpd)
    phi_578 = Factor({'x5', 'x7', 'x8'}, cpd)

    factors = [phi_1, phi_2, phi_13, phi_24, phi_25, phi_68, phi_348, phi_578]
    print(variable_elimination(factors, ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7']))
