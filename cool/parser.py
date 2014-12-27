import ply.lex as lex
import ply.yacc as yacc
import logging
import sys
import os.path as osp

keywords = {
    'class' : 'CLASS',
    'case' : 'CASE',
    'else' : 'ELSE',
    'esac' : 'ESAC',
    'fi' : 'FI',
    'if' : 'IF',
    'in' : 'IN',
    'inherits' : 'INHERITS',
    'isvoid' : 'ISVOID',
    'let' : 'LET',
    'loop' : 'LOOP',
    'new' : 'NEW',
    'not' : 'NOT',
    'of' : 'OF',
    'pool' : 'POOL',
    'then' : 'THEN',
    'while' : 'WHILE',
}

tokens = [
    'OBJECTID',
    'TYPEID',
    'INT_CONST',
    'BOOL_CONST',
    'STR_CONST',
    'NEWLINE',
    'COMMENT_SINGLELINE',
    'COMMENT_MULTILINE',
    'ASSIGN',
    'LE',
    'DARROW',
    #'ERRORTOKEN' need to return error token in cool
] + list(keywords.values())

literals = [
    ';', ',', ':', '.',
    '(', ')', '{', '}',
    '+', '-', '*', '/',
    '~', '<', '=', '@', 
]

t_ASSIGN = r'<-'
t_LE = r'<='
t_DARROW = '=>'

t_ignore = ' \f\t\v\r' # whitespace
t_ignore_COMMENT_SINGLELINE = r'[-][-].*'

def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_OBJECTID(t):
    r'[a-zA-Z][\w]*'

    #if t.value not in ['SELF_TYPE'] and t.value[0].isupper():
    if t.value[0].isupper():
        t.type = 'TYPEID'
    else:
        if t.value.casefold() in ['true', 'false']:
            t.type = 'BOOL_CONST'
            t.value = t.value.lower()
        else:
            t.type = keywords.get(t.value, 'OBJECTID')
    return t

def t_STR_CONST(t):
    r'\"([\\].|[^"\n])*\"'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMMENT_MULTILINE(t):
    r'\(\*(.|\n)*?\*\)'
    t.lexer.lineno += t.value.count('\n')
    
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    #t.value = '\n'
    #return t

def find_column(t):
    last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (t.lexpos - last_cr) + 1
    return column

def t_error(t):
    print("ERROR: Lexer: Illegal character"\
          " '{0}', linum: {1}, column: {2}".format(t.value[0],
                                                   t.lexer.lineno,
                                                   find_column(t)),
          file=sys.stderr)
    t.lexer.skip(1)
    raise Exception(t)

lexer = lex.lex(#module=lexer_rules,
                debug=1,
                lextab='gencmd_lextab',
                debuglog=logging.getLogger(''))
                #errorlog=logging.getLogger('')) 

def _get_string(arg):
    '''arg : can be a filename or string'''

    if osp.isfile(arg):
        with open(arg, 'r') as f:
            return  ''.join(f)
    else:
        return arg

def tokenize(input_str):
    '''
    This function uses the lexer and tokenizes
    the given input string'''

    result = list()
    lexer.lineno = 1
    lexer.input(input_str)
    for tok in lexer:
        if not tok:
            break
        else:
            result.append((tok.type, tok.value, lexer.lineno))
    return result


def p_program(p):
    '''program : class ';' program'''

def p_program_single(p):
    '''program : class ';' '''

def p_class(p):
    '''class : CLASS TYPE parent '{' features '}' '''
    
def p_parent(p):
    '''parent : inherits TYPE'''

def p_parent_empty(p):
    '''parent : empty'''

def p_features(p):
    '''features : feature ';' features'''
    
def p_features_empty(p):
    '''features : empty'''

def p_feature_method(p):
    '''feature : OBJECTID '(' formalargs ')' ':' TYPEID '{' expr '}' '''

def p_feature_member(p):
    '''feature : variabledeclaration '''

def p_variabledeclaration(p):
    ''' variabledeclaration : variable variableinit '''

def p_variable(p):
    ''' variable : OBJECTID ':' TYPEID '''
    
def p_variableinit(p):
    '''variableinit : ASSIGN expr '''
    
def p_variableinit_empty(p):
    '''variableinit : empty '''
    
def p_formalargs(p):
    '''formalargs : formal ',' formalargs '''

def p_formalargs_singal(p):
    '''formalargs : formal '''

def p_formalargs_empty(p):
    '''formalargs : empty '''

def p_formal(p):
    '''formal : variable '''

def p_expr_assignment(p):
    '''expr : OBJECTID ASSIGN expr'''

def p_expr_methodcall(p):
    '''expr : expr typecast '.' OBJECTID '(' actualargs ')' '''

def p_expr_functioncall(p):
    '''expr : OBJECTID '(' actualargs ')' '''

def p_typecast(p):
    '''typecast : '@' TYPEID '''
    
def p_typecast_empty(p):
    '''typecast : empty '''
    p[0] = None

def p_actualargs(p):
    '''actualargs : expr ',' actualargs '''
    
def p_actualargs_single(p):
    '''actualargs : expr '''
    
def p_actualargs_empty(p):
    '''actualargs : empty '''

def p_ifthenelse(p):
    '''ifthenelse : IF expr THEN expr ELSE expr FI '''

def p_whileloop(p):
    '''whileloop : WHILE expr LOOP expr POOL '''

def p_block(p):
    '''block : blockstatements'''

def p_blockstatements(p):
    '''blockstatements : expr ';' blockstatements'''

def p_blockstatements_single(p):
    '''blockstatements : expr ';' '''

def p_letexpr(p):
    '''letexpr : LET variablelist IN expr'''

def p_variablelist(p):
    '''variablelist : variabledeclaration ',' variablelist'''

def p_variablelist_single(p):
    '''variablelist : variabledeclaration'''

def p_case(p):
    '''case : CASE expr OF casestatements ESAC'''

def p_casestatements(p):
    '''casestatements : variable DASSIGN expr ';' casestatements'''
    
def p_casestatements_single(p):
    '''casestatements : variable DASSIGN expr ';' '''

def p_expr_unaryop_new(p):
    '''expr : NEW TYPEID'''

def p_expr_unaryop_isvoid(p):
    '''expr : ISVOID expr'''

def p_expr_unaryop_not(p):
    '''expr : NOT expr'''

def p_expr_unaryop_complement(p):
    '''expr : '~' expr'''

def p_expr_inbraces(p):
    '''expr : '(' expr ')'''

def p_expr_objectorconst(p):
    '''expr : INT_CONST
            | STR_CONST
            | BOOL_CONST
            | OBJECTID
    '''
    if isinstance(p[1], int):
        p[0] = p[1]
    elif p[1].startswith('\"') and p[1].endswith('\"'):
        p[0] = p[1][1:-1]
    elif p[1] in ['true', 'false']:
        p[0] = True if p[1] == 'true' else False
    else:
        p[0] = ObjectId(p[1])
    
def p_expr_binaryop(p):
    '''expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr '-' expr
            | expr '<' expr
            | expr LE expr
            | expr '=' expr
    '''
    p[0] = BinOp(p[2], p[1], p[3])
    
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'NOT' ),
    ('nonassoc', '<', 'LE', '='),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'ISVOID'),
    ('left', '~'),
    ('left', '@'),
    ('left', '.'),
)

    
if __name__ == '__main__':
    tokens = tokenize(_get_string(sys.argv[1]))
    #count = 1
    #print(len(tokens))

    #sys.exit(0)
    for t in tokens:
        if t[0] in keywords.values():
            print('#{0} {1}'.format(t[2], t[0]))
        elif t[0] in ['ASSIGN', 'LE', 'DARROW']:
            print('#{0} {1}'.format(t[2], t[0]))
        elif t[0] in literals:
            print("#{0} '{1}'".format(t[2], t[0]))
        else:
            print('#{0} {1} {2}'.format(t[2], t[0], t[1]))

    #print(_get_string(sys.argv[1]))
    