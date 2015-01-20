import cool
import cool.symantic_analyzer as symantic_analyzer

import pytest

class TestTypeChecker:

    def test_case1(self):
        compiler = cool.Compiler()
        fileset = ['resources/synthetic/book_list_2.cl']
        classes = compiler.parse_fileset(fileset)

        sa = symantic_analyzer.TypeChecker(classes)
        
        #with pytest.raises(symantic_analyzer.TypeCheckingException):
        #sa.type_check('Book')
        #assert True

        #sa.type_check('Silly')
        #sa.type_check('Sally')
        sa.type_check('Main')
        
if __name__ == '__main__':
    ttc = TestTypeChecker()
    ttc.test_case1()
    
