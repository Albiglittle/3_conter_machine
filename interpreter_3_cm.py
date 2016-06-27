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


def opt_code2(file):
    """optimize input code counter machine"""
    f = file.read()
    f = re.sub(r'^', '(', f)
    f = re.sub(r'$', ')', f)
    f = re.sub(r' |\n', '', f)
    f = re.sub('i', '"i",', f)
    f = re.sub('j', '"j",', f)
    f = re.sub('k', '"k",', f)
    f = re.sub(r'"i",nc', 'inc', f)
    f = re.sub(r'inc"i"', '("inc","i")', f)
    # (inc i)
    # (inc j)
    # (zero i ? ((zero j ? ((zero k ? ((inc k)) : ((dec k)))) : ((zero k ? ((inc k)) : ((dec k)))) )) : ((dec i)) )
    # (inc k)
    # (stop)

    f = re.sub(r'inc"j"', '("inc","j")', f)
    f = re.sub(r'inc"k"', '("inc","k")', f)
    f = re.sub(r'dec"i"', '("dec","i")', f)
    f = re.sub(r'dec"j"', '("dec","j")', f)
    f = re.sub(r'dec"k"', '("dec","k")', f)
    f = re.sub('stop', '("stop")', f)
    f = re.sub(r'\?zero', '(("zero",', f)
    f = re.sub(r':zero', ':(("zero",', f)
    f = re.sub(r',zero', '("zero",', f)
    f = re.sub(r'\?', '(', f)
    f = re.sub(r'\),:', ')),:', f)
    f = re.sub(r':\("', ':(("', f)
    f = re.sub(r'\)\(', '),(', f)

    f = re.sub(r':\(\("dec","i"\),', ':(("dec","i"))),', f)
    f = re.sub(r':\(\("dec","j"\),', ':(("dec","j"))),', f)
    f = re.sub(r':\(\("dec","k"\),', ':(("dec","k"))),', f)

    f = re.sub(r':\(\("dec","i"\)\(', ':(("dec","i"))),(', f)
    f = re.sub(r':\(\("dec","j"\)\(', ':(("dec","j"))),(', f)
    f = re.sub(r':\(\("dec","k"\)\(', ':(("dec","k"))),(', f)

    f = re.sub(r':\(\("inc","i"\),', ':(("inc","i"))),', f)
    f = re.sub(r':\(\("inc","j"\),', ':(("inc","j"))),', f)
    f = re.sub(r':\(\("inc","k"\),', ':(("inc","k"))),', f)

    f = re.sub(r':\(\("inc","i"\)\(', ':(("inc","i"))),(', f)
    f = re.sub(r':\(\("inc","j"\)\(', ':(("inc","j"))),(', f)
    f = re.sub(r':\(\("inc","k"\)\(', ':(("inc","k"))),(', f)

    list = []
    bum = []
    for m in re.finditer(r"zero|:", f):
        list.append([m.group(0), m.start(), m.end()])
    #print(list)
    scobe = 0
    for elem in list:
        #print(elem[0])
        if elem[0] == 'zero':
            bum.append(scobe)
            scobe += 2
            #print(bum)
        elif elem[0] == ":":
            scobe = 0
            elem.append(min(bum))
            #print(min(bum))
            bum.remove(min(bum))
            #print(bum)
        elif not bum:
            scobe = 0
    list = [elem for elem in list if elem[0] == ':']
    #print(list)
    for elem in reversed(list):
        changed = '{0}'.format(f[elem[1]-1:elem[2]])
        #print(changed)
        scobs = '{0},'.format(')'*elem[3])
        #print(scobs)
        f = f[:elem[1]-1]+'{0},'.format(')'*elem[3])+f[elem[2]:]

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


main(opt_code2(open('pr.txt', 'r')))
