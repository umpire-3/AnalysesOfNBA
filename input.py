import ply.lex as lex, \
    ply.yacc as yacc

reserved = [
    'Automaton',
    'States',
    'InitialStates',
    'FinalStates',
    'Alphabet',
    'TransitionRelation',
]

tokens = (
    'Set',
    'Relation',
    'name',
    'eq',
    'comma',
    'lbrace',
    'rbrace',
    'lparen',
    'rparen',
)

t_eq = r'='
t_comma = r','
t_lbrace = r'\{'
t_rbrace = r'\}'
t_lparen = r'\('
t_rparen = r'\)'

t_ignore = r'[ t]'


def t_name(token):
    r'[a-zA-Z0-9]+'
    if token.value in reserved:
        if token.value == 'TransitionRelation':
            token.type = 'Relation'
        else:
            token.type = 'Set'
    return token


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print('An error was occurred')

lex.lex()


def p_automaton(p):
    'automaton : Set eq lbrace sets rbrace'
    p[0] = p[4]


def p_set_stmnt(p):
    """ set_stmnt : Set eq set
                  | Relation eq relation """
    p[0] = (p[1], p[3])


def p_sets(p):
    """ sets : set_stmnt comma sets
             | set_stmnt """
    if len(p) == 2:
        p[0] = {
            p[1][0]: p[1][1]
        }
    else:
        p[0] = dict(p[3])
        p[0][p[1][0]] = p[1][1]


def p_tuple(p):
    """ tuple     : name comma tuple
                  | name """
    if len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        p[0] = (p[1],)


def p_set(p):
    """ set : lbrace tuple rbrace """
    p[0] = set(p[2])


def p_ttuple(p):
    """ ttuple   : lparen tuple rparen comma ttuple
                 | lparen tuple rparen """
    if len(p) == 4:
        p[0] = (p[2],)
    else:
        p[0] = (p[2],) + p[5]


def p_transition(p):
    """ relation : lbrace ttuple rbrace """
    p[0] = set(p[2])

parser = yacc.yacc()


with open('input.txt') as file:
    data = parser.parse(file.read())
