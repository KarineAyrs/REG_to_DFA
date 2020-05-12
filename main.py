from RegularToDFA import RegularToDFA

file_name = 'in.txt'
reg_exps = []
with open(file_name, 'r') as file:
    for line in file:
        reg_exps.append(line.rstrip())

out_file1 = 'automata1.csv'
out_file2 = 'automata2.csv'

automata1 = RegularToDFA(reg_exps[0], out_file1)
automata2 = RegularToDFA(reg_exps[1], out_file2)
