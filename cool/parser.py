import logging
import sys
import os.path as osp

from .model import *

class CoolLexer(object):

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

    def t_INT_CONST(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    def t_OBJECTID(self, t):
        r'[a-zA-Z][\w]*'

        #if t.value not in ['SELF_TYPE'] and t.value[0].isupper():
        if t.value[0].isupper():
            t.type = 'TYPEID'
        else:
            if t.value.casefold() in ['true', 'false']:
                t.type = 'BOOL_CONST'
                t.value = t.value.lower()
            else:
                t.type = CoolLexer.keywords.get(t.value, 'OBJECTID')
        return t

    def t_STR_CONST(self, t):
        r'\"([\\].|[^"\n])*\"'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_COMMENT_MULTILINE(self, t):
        r'\(\*(.|\n)*?\*\)'
        t.lexer.lineno += t.value.count('\n')

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    @classmethod
    def find_column(cls, t):
        last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (t.lexpos - last_cr) + 1
        return column

    def t_error(self, t):
        print("ERROR: Lexer: Illegal character"\
              " '{0}', linum: {1}, column: {2}".format(t.value[0],
                                                       t.lexer.lineno,
                                                       CoolLexer.find_column(t)),
              file=sys.stderr)
        t.lexer.skip(1)
        raise Exception(t)

#########################################################

class CoolParser(object):

    tokens = CoolLexer.tokens

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

    def p_program(self, p):
        '''program : class ';' program'''
        p[0] = [p[1]] + p[3]

    def p_program_single(self, p):
        '''program : class ';' '''
        p[0] = [p[1]]

    def p_class(self, p):
        '''class : CLASS TYPEID baseclass '{' features '}' '''
        p[0] = ClassDefinition(p[2], p[3], p[5])

    def p_baseclass(self, p):
        '''baseclass : INHERITS TYPEID'''
        p[0] = p[2]

    def p_baseclass_empty(self, p):
        '''baseclass : empty'''
        p[0] = None

    def p_features(self, p):
        '''features : feature ';' features'''
        p[0] = [p[1]] + p[3]

    def p_features_empty(self, p):
        '''features : empty'''
        p[0] = []

    def p_feature(self, p):
        '''feature : variabledefinition
                   | methoddefinition'''
        p[0] = p[1]

    def p_method_definition(self, p):
        '''methoddefinition : OBJECTID '(' formalargs ')' ':' TYPEID '{' expr '}' '''
        p[0] = MethodDefinition(p[1], p[3], p[6], p[8])

    def p_variabledefinition(self, p):
        '''variabledefinition : variabledeclaration variableinitialization'''
        p[0] = VariableDefinition(p[1], p[2])

    def p_variabledeclaration(self, p):
        ''' variabledeclaration : OBJECTID ':' TYPEID '''
        p[0] = VariableDeclaration(p[1], p[3])

    def p_variableinitialization(self, p):
        '''variableinitialization : ASSIGN expr '''
        p[0] = p[2]

    def p_variableinitialization_empty(self, p):
        '''variableinitialization : empty '''
        p[0] = None

    def p_formalargs(self, p):
        '''formalargs : variabledeclaration ',' formalargs'''
        p[0] = [p[1]] + p[3]

    def p_formalargs_singal(self, p):
        '''formalargs : variabledeclaration'''
        p[0] = [p[1]]

    def p_formalargs_empty(self, p):
        '''formalargs : empty '''
        p[0] = []

    def p_actualargs(self, p):
        '''actualargs : expr ',' actualargs '''
        p[0] = [p[1]] + p[3]

    def p_actualargs_single(self, p):
        '''actualargs : expr '''
        p[0] = [p[1]]

    def p_actualargs_empty(self, p):
        '''actualargs : empty '''
        p[0] = []

    def p_expr(self, p):
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

    def p_expr_unaryop_new(self, p):
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
            p[0] = ComplementExpression(True, p[2])
        elif p[1] == '~':
            p[0] = ComplementExpression(False, p[2])
        else:
            p[0] = InBracketsExpression(p[2])

    def p_expr_binaryop(self, p):
        '''expr : expr '+' expr
                | expr '-' expr
                | expr '*' expr
                | expr '/' expr
                | expr '<' expr
                | expr LE expr
                | expr '=' expr
        '''
        p[0] = BinaryOperationExpression(p[2], p[1], p[3])

    def p_expr_object_or_const(self, p):
        '''expr : INT_CONST
                | STR_CONST
                | BOOL_CONST
                | OBJECTID
        '''
        if isinstance(p[1], int):
            p[0] = NumberExpression(p[1])
        elif p[1].startswith('\"') and p[1].endswith('\"'):
            p[0] = StringExpression(p[1][1:-1])
        elif p[1] in ['true', 'false']:
            p[0] = BooleanExpression(True if p[1] == 'true' else False)
        else:
            p[0] = ObjectIdExpression(p[1])

    def p_assignment(self, p):
        '''assignment : OBJECTID ASSIGN expr'''
        p[0] = Assignment(p[1], p[3])

    def p_letexpr(self, p):
        '''letexpr : LET variablelist IN expr'''
        p[0] = LetExpression(p[2], p[4])

    def p_method_invoke(self, p):
        '''methodinvoke : expr DOT OBJECTID '(' actualargs ')' '''
        p[0] = MethodInvoke(p[1], None, p[3], p[5])

    def p_method_invoke_with_typecast(self, p):
        '''methodinvoke : expr '@' TYPEID DOT OBJECTID '(' actualargs ')' '''
        p[0] = MethodInvoke(p[1], p[3], p[5], p[7])

    def p_local_method_invoke(self, p):
        '''localmethodinvoke : OBJECTID '(' actualargs ')' '''
        p[0] = MethodInvoke(None, None, p[1], p[3])

    def p_ifthenelse(self, p):
        '''ifthenelse : IF expr THEN expr ELSE expr FI '''
        p[0] = IfThenElse(p[2], p[4], p[6])

    def p_whileloop(self, p):
        '''whileloop : WHILE expr LOOP expr POOL '''
        p[0] = WhileLoop(p[2], p[4])

    def p_block(self, p):
        '''blockexpr : '{' blockstatements '}' '''
        p[0] = BlockStatement(p[2])

    def p_blockstatements(self, p):
        '''blockstatements : expr ';' blockstatements'''
        p[0] = [p[1]] + p[3]

    def p_blockstatements_single(self, p):
        '''blockstatements : expr ';' '''
        p[0] = [p[1]]

    def p_variablelist(self, p):
        '''variablelist : variabledefinition ',' variablelist'''
        p[0] = [p[1]] + p[3]

    def p_variablelist_single(self, p):
        '''variablelist : variabledefinition'''
        p[0] = [p[1]]

    def p_case(self, p):
        '''caseexpr : CASE expr OF casestatements ESAC'''
        p[0] = CaseExpression(p[2], p[4])

    def p_casestatements(self, p):
        '''casestatements : variabledeclaration DARROW expr ';' casestatements'''
        p[0] = [CaseStatement(p[1], p[3])] + p[5]

    def p_casestatements_single(self, p):
        '''casestatements : variabledeclaration DARROW expr ';' '''
        p[0] = [CaseStatement(p[1], p[3])]

    def p_empty(self, p):
        '''empty : '''
        pass

    def p_error(self, p):
        print("Syntax error at '{0}'", p)
        raise Exception(p)

        
    