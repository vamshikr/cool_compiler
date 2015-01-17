import os
import os.path as osp
import pytest
import cool

class TestMain:

    @classmethod
    def test_cool_parser(cls, filename):
        #filename = './test/resources/examples/book_list.cl'
        print(os.getcwd())
        compiler = cool.Compiler()
        if osp.isfile(filename):
            ast = compiler.parse_file(filename)
            print(ast)
            assert ast != None
        else:
            assert osp.isfile(filename)

class TestSymanticAnalyzer:

    #Multiple class file definition
    #Multiple method definitions
    #
    #Incorrect inheritance

    
    pass

if __name__ == '__main__':
    import sys
    import os.path as osp
    
    for filename in sys.argv[1:]:
        if osp.isfile(filename):
            TestMain.test_cool_parser(filename)
