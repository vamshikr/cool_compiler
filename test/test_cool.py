import os
import os.path as osp
import pytest
import cool

class TestMain:


    def test_cool_parser(self):
        filename = './test/resources/examples/book_list.cl'
        print(os.getcwd())
        self.compiler = cool.Compiler()
        if osp.isfile(filename):
            ast = self.compiler.parse_file(filename)
            print(ast)
            assert ast != None
        else:
            assert osp.isfile(filename)
