import ply.lex as lex
import ply.yacc as yacc
import logging
import sys
import os.path as osp

from model import *

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
    'DOT',
    #'ERRORTOKEN' need to return error token in cool
] + list(keywords.values())

literals = [
    ';', ',', ':',
    '(', ')', '{', '}',
    '+', '-', '*', '/',
    '~', '<', '=', '@', 
]

t_ASSIGN = r'<-'
t_LE = r'<='
t_DARROW = '=>'
t_DOT=r'\.'

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

#########################################################

precedence = (
    ('right', 'IN'),
    ('right', 'ASSIGN'),
    ('left', 'NOT' ),
    ('nonassoc', '<', 'LE', '='),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'ISVOID'),
    ('left', '~'),
    ('left', '@'),
    ('left', 'DOT'),
)

def p_program(p):
    '''program : class ';' program'''
    p[0] = [p[1]] + p[3]
    
def p_program_single(p):
    '''program : class ';' '''
    p[0] = [p[1]]
    
def p_class(p):
    '''class : CLASS TYPEID baseclass '{' features '}' '''
    p[0] = ClassDefinition(p[2], p[3], p[5])
    
def p_baseclass(p):
    '''baseclass : INHERITS TYPEID'''
    p[0] = p[2]
    
def p_baseclass_empty(p):
    '''baseclass : empty'''
    p[0] = None

def p_features(p):
    '''features : feature ';' features'''
    p[0] = [p[1]] + p[3]

def p_features_empty(p):
    '''features : empty'''
    p[0] = []

def p_feature(p):
    '''feature : variabledefinition
               | methoddefinition'''
    p[0] = p[1]
    
def p_method_definition(p):
    '''methoddefinition : OBJECTID '(' formalargs ')' ':' TYPEID '{' expr '}' '''
    p[0] = MethodDefinition(p[1], p[3], p[6], p[8])

def p_variabledefinition(p):
    '''variabledefinition : variabledeclaration variableinitialization'''
    p[0] = VariableDefinition(p[1], p[2])
    
def p_variabledeclaration(p):
    ''' variabledeclaration : OBJECTID ':' TYPEID '''
    p[0] = VariableDeclaration(p[1], p[3])
    
def p_variableinitialization(p):
    '''variableinitialization : ASSIGN expr '''
    p[0] = p[2]
    
def p_variableinitialization_empty(p):
    '''variableinitialization : empty '''
    p[0] = None
    
def p_formalargs(p):
    '''formalargs : variabledeclaration ',' formalargs'''
    p[0] = [p[1]] + p[3]
    
def p_formalargs_singal(p):
    '''formalargs : variabledeclaration'''
    p[0] = [p[1]]

def p_formalargs_empty(p):
    '''formalargs : empty '''
    p[0] = []
    
def p_actualargs(p):
    '''actualargs : expr ',' actualargs '''
    p[0] = [p[1]] + p[3]

def p_actualargs_single(p):
    '''actualargs : expr '''
    p[0] = [p[1]]

def p_actualargs_empty(p):
    '''actualargs : empty '''
    p[0] = []

def p_expr(p):
    '''expr : assignment
            | methodinvoke
            | localmethodinvoke
            | ifthenelse
            | whileloop
            | blockexpr
            | letexpr
            | caseexpr
    '''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : OBJECTID ASSIGN expr'''
    p[0] = Assignment(p[1], p[3])
    
def p_letexpr(p):
    '''letexpr : LET variablelist IN expr'''
    p[0] = LetExpression(p[2], p[4])
    
def p_method_invoke(p):
    '''methodinvoke : expr DOT OBJECTID '(' actualargs ')' '''
    p[0] = MethodInvoke(p[1], None, p[3], p[5])
    
def p_method_invoke_with_typecast(p):
    '''methodinvoke : expr '@' TYPEID DOT OBJECTID '(' actualargs ')' '''
    p[0] = MethodInvoke(p[1], p[2], p[4], p[6])
    
def p_local_method_invoke(p):
    '''localmethodinvoke : OBJECTID '(' actualargs ')' '''
    p[0] = LocalMethodInvoke(p[1], p[3])

def p_ifthenelse(p):
    '''ifthenelse : IF expr THEN expr ELSE expr FI '''
    p[0] = IfThenElse(p[2], p[4], p[6])
    
def p_whileloop(p):
    '''whileloop : WHILE expr LOOP expr POOL '''
    p[0] = WhileLoop(p[2], p[4])
    
def p_block(p):
    '''blockexpr : '{' blockstatements '}' '''
    p[0] = BlockStatement(p[2])
    
def p_blockstatements(p):
    '''blockstatements : expr ';' blockstatements'''
    p[0] = [p[1]] + p[3]
    
def p_blockstatements_single(p):
    '''blockstatements : expr ';' '''
    p[0] = [p[1]]

def p_variablelist(p):
    '''variablelist : variabledefinition ',' variablelist'''
    p[0] = [p[1]] + p[3]
    
def p_variablelist_single(p):
    '''variablelist : variabledefinition'''
    p[0] = [p[1]]

def p_case(p):
    '''caseexpr : CASE expr OF casestatements ESAC'''
    p[0] = CaseExpression(p[2], p[4])
    
def p_casestatements(p):
    '''casestatements : variabledeclaration DARROW expr ';' casestatements'''
    p[0] = [CaseStatement(p[1], p[3])] + p[5]
    
def p_casestatements_single(p):
    '''casestatements : variabledeclaration DARROW expr ';' '''
    p[0] = [CaseStatement(p[1], p[3])]

def p_expr_unaryop_new(p):
    '''expr : NEW TYPEID
            | ISVOID expr
            | NOT expr
            | '~' expr
            | '(' expr ')'
    '''
    if p[1] == 'new':
        p[0] = NewStatement(p[2])
    elif p[1] == 'isvoid':
        p[0] = IsVoidExpression(p[2])
    elif p[1] == 'not':
        p[0] = Complement(true, p[2])
    elif p[1] == '~':
        p[0] = Complement(false, p[2])
    else:
        p[0] = InBracketsExpression(p[2])
        
def p_expr_binaryop(p):
    '''expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr '<' expr
            | expr LE expr
            | expr '=' expr
    '''
    p[0] = BinaryOperationExpression(p[2], p[1], p[3])

def p_expr_object_or_const(p):
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
        p[0] = ObjectIdExpression(p[1])

def p_empty(p):
    '''empty : '''
    pass
    
def p_error(p):
    print("Syntax error at '{0}'", p)

parser = yacc.yacc(debug=True,
                   tabmodule='cool_parsetab',
                   start='program',
                   debugfile='cool_parser.out')

def parse_str(input_str):
    '''Returns AST'''
    return parser.parse(input_str, lexer=lexer)

def parse_file(filename):
    input_str = _get_string(filename)
    return parse_str(input_str)
    
if __name__ == '__main__':
    print(parse_file(sys.argv[1]))
    
    
if __name__ == '__mai__':
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
    