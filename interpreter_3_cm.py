"""Interpreter for a mini-language of 3-counter machine."""
import re

ns = {}      # ns holds the program's variable names

global ans


def interpretCLIST(p) :
    """pre: p  is a program represented as a  CLIST ::=  [ CTREE+ ]
                  where  CTREE+  means  one or more CTREEs
       post:  ns  holds all the updates commanded by program  p
    """
    for command in p:
        interpretCTREE(command)


def interpretCTREE(c):
    """pre: c  is a command represented as a CTREE:
         CTREE ::= ["zero", ETREE, CLIST, CLIST] | stop | ETREE
       post:  ns  holds all the updates commanded by  c
    """
    operator = c[0]

    if operator == "zero":  # zero command
        expr = c[1]
        body_true = c[2]
        body_false = c[3]

        if interpretETREE(expr) == 0:
            interpretCLIST(body_true)
        else:
            interpretCLIST(body_false)

    elif operator == "stop":
        print(ns)
        exit()

    else:
        interpretETREE(c)


def interpretETREE(e):
    """pre: e  is an expression represented as an ETREE:
           ETREE ::=  VAR  |  [UNOP, ETREE]
                      where UNOP is either "inc" or "dec"
      post:  ans  holds the numerical value of  e
      returns:   ans
    """

    if isinstance(e, str) and len(e) > 0 and e[0].isalpha():  # var name
        if e in ns:   # see if variable name is defined
            ans = ns[e]  # look up its value
        else:
            crash("variable name undefined")
    else:
        unop = e[0]  # get operator
        ans = interpretETREE(e[1])  # get value of arg
        var = e[1]  # get arg
        if unop == "inc":
            ns[var] = ans + 1  # do the assignment
        elif unop == "dec":
            if ans:
                ns[var] = ans - 1  # do the assignment
            else:
                crash("decrement zero")
        else:
            crash("illegal arithmetic operator")
    return ans


def crash(message):
    """pre: message is a string
       post: message is printed and interpreter stopped
    """
    print message + "! crash! core dump: ", ns
    raise Exception   # stops the interpreter


def opt_code(file):
    """optimize input code counter machine"""
    f = file.read()
    f = re.sub(r'^', '(', f)
    f = re.sub(r'$', ')', f)
    f = re.sub('i', '"i",', f)
    f = re.sub('j', '"j",', f)
    f = re.sub('k', '"k",', f)
    f = re.sub(r'"i",nc', 'inc', f)
    f = re.sub(r'inc', '"inc",', f)
    f = re.sub(r'dec', '"dec",', f)
    f = re.sub(r'zero', '"zero",', f)
    f = re.sub('stop', '"stop"', f)
    f = re.sub(',\)', ')', f)
    f = re.sub(r' |\n|\?', '', f)
    f = re.sub(r'\)\(|\):\(', '),(', f)
    f = re.sub('\)', ']', f)
    f = re.sub('\(', '[', f)

    return eval(f)


def main(program):
    """pre:  program is a  PTREE ::=  CLIST
       post:  ns  holds all updates within  program
    """
    global ns, ans  # ns & ans are globals to main
    ns = {'i': 0, 'j': 0, 'k': 0}
    interpretCLIST(program)
    print "final namespace =", ns


main(opt_code(open('pr.txt', 'r')))
