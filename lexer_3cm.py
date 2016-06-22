import ply.lex as lex
import re

tokens = (
    'INC', 'DEC', 'ZERO', 'STOP', 'QUEST', 'COLON', 'OPEN', 'CLOSE', 'COUNTER'
)

t_INC = r'inc'
t_COUNTER = r'I|J|K'
t_DEC = r'dec'
t_ZERO = r'zero'
t_QUEST = r'\?'
t_COLON = r':'
t_OPEN = r'\('
t_CLOSE = r'\)'
t_STOP = r'stop'

t_ignore = ' \r\t\f'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.UNICODE | re.DOTALL)

data = open('pr', 'r').read()

lexer.input(data)

output = open('nodes_and_asm.txt', 'w')

while True:
    tok = lexer.token()
    if not tok:
        break
    output.write(str(tok)+'\n')
output.close()
