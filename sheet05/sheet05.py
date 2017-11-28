
factortable = {
    (1, 2): {
        (True, True): 0.5,
        (True, False): 0.3,
        (False, True): 0.1,
        (False, False): 0.7
    },
    (1, 3): {
        (True, True): 0.2,
        (True, False): 0.1,
        (False, True): 0.2,
        (False, False): 0.7
    },
    (1, 4): {
        (True, True): 0.3,
        (True, False): 0.3,
        (False, True): 0.3,
        (False, False): 0.3
    },
    (2, 5): {
        (True, True): 0.8,
        (True, False): 0.4,
        (False, True): 0.5,
        (False, False): 0.8
    },
    (2, 6): {
        (True, True): 1.0,
        (True, False): 0.5,
        (False, True): 0.5,
        (False, False): 0.9
    },
    (3, 7): {
        (True, True): 0.5,
        (True, False): 0.3,
        (False, True): 0.1,
        (False, False): 0.1
    },
    (3, 8): {
        (True, True): 0.1,
        (True, False): 0.4,
        (False, True): 0.1,
        (False, False): 0.1
    },
    (3, 9): {
        (True, True): 0.7,
        (True, False): 0.7,
        (False, True): 0.1,
        (False, False): 0.2
    },
    (4, 10): {
        (True, True): 0.5,
        (True, False): 0.8,
        (False, True): 0.5,
        (False, False): 0.3
    },
    (5, 11): {
        (True, True): 0.5,
        (True, False): 0.8,
        (False, True): 0.6,
        (False, False): 0.1
    },
    (7, 12): {
        (True, True): 0.9,
        (True, False): 0.9,
        (False, True): 0.9,
        (False, False): 0.4
    },
    (10, 13): {
        (True, True): 0.9,
        (True, False): 0.1,
        (False, True): 0.5,
        (False, False): 0.5
    },
    (10, 14): {
        (True, True): 0.3,
        (True, False): 0.2,
        (False, True): 0.1,
        (False, False): 0.5
    }
}


class Node(object):
    def __init__(self, identifier, parent, table):
        self.identifier = identifier
        self.parent = parent
        self.table = table
        self.children = []
        self.upward_message = None

    def _sum_out(self, x):
        if not self.parent:
            return 1
        values = self.table[(self.parent.identifier, self.identifier)]
        return values[(True, x)] + values[(False, x)]

    def make_childs_from_table(self):
        """
        Build the tree from the keys of the factor table.
        """
        self.children = [Node(child, self, self.table) for x, child in self.table.keys() if x == self.identifier]
        for child in self.children:
            child.make_childs_from_table()

    def pass_upward(self):
        """
        Calculate the upward pass message.

        :return: A tuple of the positive and negative message factors.
        """
        factor_beta_pos, factor_beta_neg = self._sum_out(True), self._sum_out(False)
        for child in self.children:
            msg_child = child.pass_upward()
            factor_beta_pos *= msg_child[0]
            factor_beta_neg *= msg_child[1]

        return factor_beta_pos, factor_beta_neg

    def pass_downward(self):
        pass

    def __repr__(self):
        return "Node(" + str(self.identifier) + ")"

if __name__ == '__main__':
    root = Node(1, None, factortable)
    root.make_childs_from_table()
    print(root.pass_upward())
