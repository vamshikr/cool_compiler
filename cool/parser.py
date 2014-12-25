import ply.lex as lex
import ply.yacc as yacc
import logging
import sys
import os.path as osp


keywords = {
    'Class' : 'CLASS', 
    'else' : 'ELSE', 
    'false' : 'FALSE', 
    'fi' : 'FI', 
    'if' : 'IF', 
    'in' : 'IN', 
    'inherits' : 'INHERITS', 
    'isvoid' : 'ISVOID', 
    'let' : 'LET', 
    'loop' : 'LOOP', 
    'pool' : 'POOL', 
    'then' : 'THEN', 
    'while' : 'WHILE', 
    'case' : 'CASE', 
    'esac' : 'ESAC', 
    'new' : 'NEW', 
    'of' : 'OF', 
    'not' : 'NOT', 
    'true' : 'TRUE', 
}

tokens = [
    'INTEGER',
    'ID',
    'TYPE',
    'STRING',
    'NEWLINE',
    'COMMENT_SINGLELINE',
    'COMMENT_MULTILINE',
    'ASSIGNMENT',
    'LTEQ',
    'GTEQ',
    #'ERRORTOKEN' need to return error token in cool
] + list(keywords.values())

literals = [
    ';', ',', ':', '.',
    '(', ')', '{', '}',
    '+', '-', '*', '/',
    '~', '<', '>',
    '=', '@', 
]

t_ASSIGNMENT = r'<-'
t_LTEQ = r'<='
t_GTEQ = '>='

t_ignore = ' \f\t\v\r' # whitespace


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_ID(t):
    r'[a-zA-Z][\w]*'

    if t.value not in ['SELF_TYPE', 'Class'] and \
       t.value[0].isupper():
        t.type = 'TYPE'
    else:
        if t.value.casefold() in ['true', 'false']:
            t.type = t.value.upper()
            t.value = t.value.lower()
        else:
            t.type = keywords.get(t.value, 'ID')
    return t

def t_STRING(t):
    r'\"([\\].|[^"\n])*\"'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMMENT_SINGLELINE(t):
    r'[-][-].*'

def t_COMMENT_MULTILINE(t):
    #r'[(][*](.|\n)*[*][)]'
    r'\(\*(.|\n)*?\*\)'
    t.lexer.lineno += t.value.count('\n')

    #t.lexer.lineno += t.value.count('\n')
    print('COMMENT_MULTILINE: ', t)
    
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
            result.append((tok.type, tok.value))
    return result

if __name__ == '__main__':
    print(tokenize(_get_string(sys.argv[1])))
    #print(_get_string(sys.argv[1]))
    