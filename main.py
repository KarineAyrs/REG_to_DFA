from RegularToDFA import RegularToDFA
from equivalence_of_automatas import EquivalenceOfAutomatas

file_name = 'in.txt'
reg_exps = []
with open(file_name, 'r') as file:
    for line in file:
        reg_exps.append(line.rstrip())

out_file1 = 'automata1.csv'
out_file2 = 'automata2.csv'
automata1 = RegularToDFA(reg_exps[0], out_file1)
final_states1 = automata1.final_states

aut_df1 = automata1.automata

automata2 = RegularToDFA(reg_exps[1], out_file2)
final_states2 = automata2.final_states
aut_df2 = automata2.automata

equiv = EquivalenceOfAutomatas(final_states1, aut_df1, final_states2, aut_df2)
if equiv.equivalence_of_automatas():
    print('regular expressions are equal')
else:
    print('regular expressions are NOT equal')
