from lexer_3cm import tokens
import ply.yacc as yacc


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


def p_pr(p):
    '''pr :
          | instr pr'''
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = p[1].add_parts([p[2]])


def p_instr(p):
    '''instr : STOP
             | inc
             | dec
             | zero'''
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = Node('instr', [p[1]])


def p_zero(p):
    '''zero : ZERO COUNTER QUEST OPEN instr CLOSE COLON OPEN instr CLOSE'''
    p[0] = Node('zero', [p[2], p[5], p[9]])


def p_inc(p):
    '''inc : INC COUNTER'''
    p[0] = Node('inc', p[2])


def p_dec(p):
    '''dec : DEC COUNTER'''
    p[0] = Node('dec', p[2])


def p_error(p):
    print 'Unexpected token:', p

parser = yacc.yacc()


def build_tree(code):
    return parser.parse(code)

