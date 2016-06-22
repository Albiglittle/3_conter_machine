import parser_3cm

data = open('pr', 'r').read()
output = open('nodes_and_asm.txt', 'a')

output.write(str(parser_3cm.build_tree(data)))
