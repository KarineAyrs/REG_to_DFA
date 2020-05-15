from RegularToDFA import RegularToDFA
from equivalence_of_automatas import EquivalenceOfAutomatas
# http://cmcstuff.esyr.org/vmkbotva-r15/2%20%D0%BA%D1%83%D1%80%D1%81/4%20%D0%A1%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/%D0%9F%D1%80%D0%B0%D0%BA/%D0%94%D0%B7/regexp.pdf
# http://aliev.me/runestone/Trees/ParseTree.html
# https://neerc.ifmo.ru/wiki/index.php?title=%D0%AD%D0%BA%D0%B2%D0%B8%D0%B2%D0%B0%D0%BB%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B9_%D0%94%D0%9A%D0%90#.D0.9F.D1.80.D0.BE.D0.B2.D0.B5.D1.80.D0.BA.D0.B0_.D1.87.D0.B5.D1.80.D0.B5.D0.B7_BFS

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
























# a1 = pd.DataFrame(
#     {'A': ['c', 'd', 'c', 'd', 'c', 'd'],
#      'Q': [0, 0, 1, 1, 2, 2],
#      'Fi': [0, 1, 2, 0, 1, 2]
#      }
# )
# f_s1 = [0]
#
# a2 = pd.DataFrame(
#     {'A': ['c', 'd', 'c', 'd', 'c', 'd', 'c', 'd'],
#      'Q': [0, 0, 1, 1, 2, 2, 3, 3],
#      'Fi': [0, 1, 2, 0, 3, 2, 2, 0]
#      }
# )
# f_s2 = [0]
