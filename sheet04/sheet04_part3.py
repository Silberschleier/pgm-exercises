from libpgm.graphskeleton import GraphSkeleton
from libpgm.nodedata import NodeData
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.tablecpdfactorization import TableCPDFactorization
from copy import deepcopy


def eliminate_var(factors, variable):
    factors1 = [phi for phi in factors if variable in phi.scope]
    factors2 = [phi for phi in factors if variable not in phi.scope]

    psi = factors1[0]
    for phi in factors1[1:]:
        psi.multiplyfactor(phi)

    psi.sumout(variable)
    factors2.append(psi)
    return factors2


def variable_elimination(table, variables):
    for var in variables:
        table.factorlist = eliminate_var(table.factorlist, var)

    for phi in table.factorlist[1:]:
        table.factorlist[0].multiplyfactor(phi)

    factor = table.factorlist[0]
    table.factorlist = table.factorlist[0]
    return factor

if __name__ == '__main__':
    nd = NodeData()
    skel = GraphSkeleton()
    nd.load('table.json')
    skel.load('table.json')
    skel.toporder()

    bn = DiscreteBayesianNetwork(skel, nd)
    table = TableCPDFactorization(bn)

    output = ''
    for x in ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']:
        variables = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']
        variables.remove(x)
        temporary_table = deepcopy(table)
        factor = variable_elimination(temporary_table, variables)

        output += 'phi({}) = \t{:>10},\t{:>10}\n'.format(x, round(factor.vals[0], 2), round(factor.vals[1], 2))
    print(output)
