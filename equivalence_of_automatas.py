import pandas as pd
import numpy as np


class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second


class EquivalenceOfAutomatas:
    def __init__(self, final_states1, automata1, final_states2, automata2):
        self.final_states1 = final_states1
        self.final_states2 = final_states2
        self.automata1 = automata1
        self.automata2 = automata2

    def _is_in_pairs(self, q, p):
        for i in q:
            if i.first == p.first and i.second == p.second:
                return True
        return False

    def is_final1(self, state):
        if state in self.final_states1:
            return True
        return False

    def is_final2(self, state):
        if state in self.final_states2:
            return True
        return False

    def equivalence_of_automatas(self):
        if set(np.unique(self.automata1['A'])) != set(np.unique(self.automata2['A'])):
            return False
        alf = np.unique(self.automata1['A'])
        q = [Pair(self.automata1['Q'][0], self.automata2['Q'][0])]
        used = np.zeros((len(self.automata1['Q']) + 1, len(self.automata2['Q']) + 1))

        while q:
            pair = q.pop()
            u = pair.first
            v = pair.second

            if self.is_final1(u) != self.is_final2(v):
                return False
            used[u][v] = 1

            for i in alf:

                try:
                    s1 = self.automata1.loc[(self.automata1['Q'] == u) & (self.automata1['A'] == i)]['Fi'].values[0]
                except:
                    s1 = len(self.automata1['Q'])
                try:
                    s2 = self.automata2.loc[(self.automata2['Q'] == v) & (self.automata2['A'] == i)]['Fi'].values[0]
                except:
                    s2 = len(self.automata2['Q'])

                if used[s1][s2] == 0:
                    if not self._is_in_pairs(q, Pair(s1, s2)):
                        q.append(Pair(s1, s2))

        return True
