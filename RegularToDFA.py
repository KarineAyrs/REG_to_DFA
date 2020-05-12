import pandas as pd


class Node:
    def __init__(self, symbol=None, position=0, parent=None, left=None, right=None):
        self.symbol = symbol
        self.position = position
        self.parent = parent
        self.left = left
        self.right = right
        self.nullable = True
        self.firstpos = set()
        self.lastpos = set()

    def is_leaf(self):
        return (self.left is None) and (self.right is None)


class RegularToDFA:

    def __init__(self, reg_exp, out_file):
        self.reg_exp = reg_exp + '#'
        self.root = Node()
        self.followpos = dict()
        self.keys_symbols = dict()
        self.out = out_file
        self.count = 1
        self._build_tree()
        # self.dfs()
        self._REG_to_DKA()

    def dfs(self):  # prints syntax_tree
        s = [self.root]
        while len(s) != 0:
            u = s.pop(-1)
            print('parent=', u.symbol, u.position, u.nullable, u.firstpos, u.lastpos)
            if u.left is not None:
                print('left=', u.left.symbol, u.left.position, u.left.nullable, u.left.firstpos, u.left.lastpos)
                s.append(u.left)

            if u.right is not None:
                print('right=', u.right.symbol, u.right.position, u.right.nullable, u.right.firstpos, u.right.lastpos)
                s.append(u.right)

    def _for_convenience(self):
        new_reg = []
        for i in range(len(self.reg_exp)):
            new_reg.append(self.reg_exp[i])
            if i == len(self.reg_exp) - 1:
                break
            if self.reg_exp[i] in ['*', ')'] or self.reg_exp[i] not in ['*', '(', ')', '|']:
                if self.reg_exp[i + 1] not in ['*', ')', '|']:  # symbols and (
                    new_reg.append('.')
        return new_reg

    def _build_tree(self):
        cur_node = self.root
        reg_perfect = self._for_convenience()
        for i in range(len(reg_perfect)):
            if reg_perfect[i] == '(':
                left = Node(None, 0, cur_node, None, None)
                cur_node.left = left
                cur_node = cur_node.left
            if reg_perfect[i] in ['|', '.']:
                if cur_node.symbol is not None:
                    self._calc_everything_in_the_WORLD(cur_node)
                    parent = Node(reg_perfect[i], 0, None, cur_node, None)
                    cur_node.parent = parent
                    right_of_parent = Node(None, 0, cur_node.parent, None, None)
                    cur_node.parent.right = right_of_parent
                    self.root = cur_node.parent
                    cur_node = cur_node.parent.right
                else:
                    cur_node.symbol = reg_perfect[i]
                    right = Node(None, 0, cur_node, None, None)
                    cur_node.right = right
                    cur_node = cur_node.right
            if reg_perfect[i] == '*':
                if cur_node.symbol is not None:
                    self._calc_everything_in_the_WORLD(cur_node)
                    grand_child = cur_node.right
                    child = Node(reg_perfect[i], 0, cur_node, grand_child, None)
                    cur_node.right = child
                    self._calc_everything_in_the_WORLD(cur_node.right)
                    grand_child.parent = cur_node.right
                    self.root = cur_node
                else:
                    cur_node.symbol = reg_perfect[i]
                    self._calc_everything_in_the_WORLD(cur_node)
                    parent = Node(None, 0, None, cur_node, None)
                    cur_node.parent = parent
                    cur_node = cur_node.parent
                    self.root = cur_node

            if reg_perfect[i] == ')':
                if cur_node.parent is not None:
                    cur_node = cur_node.parent
                    self.root = cur_node

                else:
                    parent = Node(None, 0, None, cur_node, None)
                    cur_node.parent = parent
                    cur_node = cur_node.parent
                    self.root = cur_node

            if reg_perfect[i] not in ['(', ')', '|', '*', '.']:
                cur_node.symbol = reg_perfect[i]
                cur_node.position = self.count
                self.keys_symbols[self.count] = cur_node.symbol
                self.count = self.count + 1
                self._calc_everything_in_the_WORLD(cur_node)
                if cur_node.parent is not None:
                    cur_node = cur_node.parent
                    self._calc_everything_in_the_WORLD(cur_node)
                    self.root = cur_node

                else:
                    parent = Node(None, 0, None, cur_node, None)
                    cur_node.parent = parent
                    cur_node = cur_node.parent
                    self.root = cur_node
        self.followpos[self.count - 1] = set()

    def _calc_everything_in_the_WORLD(self, node):
        if node.is_leaf():
            if node.position != 0:
                node.nullable = False
                node.firstpos.add(node.position)
                node.lastpos.add(node.position)
            else:
                node.nullable = True
        else:
            if node.symbol == '|':
                if (node.left is not None) and (node.right is not None):
                    node.nullable = node.left.nullable or node.right.nullable
                    node.firstpos = node.left.firstpos | node.right.firstpos
                    node.lastpos = node.left.lastpos | node.right.lastpos
            if node.symbol == '.':
                if (node.left is not None) and (node.right is not None):
                    node.nullable = node.left.nullable and node.right.nullable
                    if node.left.nullable:
                        node.firstpos = node.left.firstpos | node.right.firstpos
                    else:
                        node.firstpos = node.left.firstpos

                    if node.right.nullable:
                        node.lastpos = node.left.lastpos | node.right.lastpos
                    else:
                        node.lastpos = node.right.lastpos
                    for i in node.left.lastpos:
                        if i in self.followpos:
                            self.followpos[i] = self.followpos[i] | node.right.firstpos
                        else:
                            self.followpos[i] = node.right.firstpos

            if node.symbol == '*':
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos
                for i in node.left.lastpos:
                    if i in self.followpos:
                        self.followpos[i] = self.followpos[i] | node.left.firstpos
                    else:
                        self.followpos[i] = node.left.firstpos

    def _REG_to_DKA(self):
        Input_sym = []
        States_Q = []
        States_D = []
        Q_nepom = [self.root.firstpos]
        Q_pomech = []
        final_state = []
        while (Q_nepom):
            R = list(Q_nepom.pop())
            Q_pomech.append(set(R))

            sym = []
            for i in R:
                sym.append(self.keys_symbols[i])

            for i in range(len(sym)):
                S = set()
                for j in range(len(sym)):
                    if sym[i] == sym[j]:
                        S = S | self.followpos[R[j]]

                if S:
                    if S not in Q_nepom and S not in Q_pomech:
                        Q_nepom.append(S)
                    Input_sym.append(sym[i])
                    States_Q.append(set(R))
                    States_D.append(S)
                    if self.count - 1 in S:
                        final_state.append(1)
                    else:
                        final_state.append(0)
        labels = [0 for i in range(len(Input_sym))]
        df = pd.DataFrame(
            {'A': Input_sym,
             'Q': States_Q,
             'Fi': States_D,
             'final_state': final_state})

        for i in range(len(df['A'])):
            for j in range(len(df['A'])):
                if df.iloc[i][0] == df.iloc[j][0] and df.iloc[i][1] == df.iloc[j][1] and df.iloc[i][2] == df.iloc[j][2] \
                        and i != j and labels[i] != 1:
                    labels[j] = 1

        df['Dub'] = labels
        df = df.loc[df['Dub'] != 1]
        df = df.drop(['Dub'], axis='columns')
        df.to_csv(self.out, index=False)
