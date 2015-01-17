__all__ = ['model', 'parser']

import os.path as osp
import ply.lex as lex
import ply.yacc as yacc
from . parser import CoolLexer
from . parser import CoolParser
import logging
import pkgutil

class Compiler():
    loaded = False

    def __init__(self):
        if Compiler.loaded == False:
            Compiler.load()
            
    @classmethod
    def load(cls):
        cls.lexer = lex.lex(module=CoolLexer(),
                        debug=1,
                        lextab='gencmd_lextab',
                        debuglog=logging.getLogger(''),
                        errorlog=logging.getLogger('')) 

        cls.parser = yacc.yacc(module=CoolParser(),
                           debug=True,
                           tabmodule='cool_parsetab',
                           start='program',
                           debugfile='cool_parser.out')
        cls.loaded = True

    def _get_string(self, arg):
        '''arg : can be a filename or string'''

        if osp.isfile(arg):
            with open(arg, 'r') as f:
                return  ''.join(f)
        else:
            return arg

    def tokenize_str(self, input_str):
        '''
        This function uses the lexer and tokenizes
        the given input string'''

        result = list()
        Compiler.lexer.lineno = 1
        Compiler.lexer.input(input_str)
        for tok in Compiler.lexer:
            if not tok:
                break
            else:
                result.append((tok.type, tok.value, Compiler.lexer.lineno))
        return result

    def tokenize_file(self, filename):
        input_str = self._get_string(filename)
        return self.tokenize_str(input_str)
        
    def parse_str(self, input_str):
        '''Returns AST'''
        return Compiler.parser.parse(input_str, lexer=Compiler.lexer)

    def parse_file(self, filename):
        input_str = self._get_string(filename)
        return self.parse_str(input_str)
    
    def parse_fileset(self, fileset):

        basic_cl = pkgutil.get_data(__name__, 'basic.cl')
        ast_list = self.parse_str(str(basic_cl, encoding='utf-8'))
        
        for filename in fileset:
            if osp.isfile(filename) and osp.splitext(filename)[1] == '.cl':
                ast = self.parse_file(filename)
                if ast is not None:
                    ast_list.extend(ast)

        return ast_list

        