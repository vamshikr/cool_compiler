import sys
import cool
import cool.symantic_analyzer as symantic_analyzer

#import pytest

class TestTypeChecker:
    compiler = cool.Compiler()

    def test_case1(self):
        fileset = ['resources/synthetic/book_list_2.cl']
        classes = TestTypeChecker.compiler.parse_fileset(fileset)

        sa = symantic_analyzer.TypeChecker(classes)
        
        #with pytest.raises(symantic_analyzer.TypeCheckingException):
        #sa.type_check('Book')
        #assert True

        #sa.type_check('Silly')
        #sa.type_check('Sally')
        sa.type_check('Main')

    def test_case2(self):
        fileset = ['resources/synthetic/example2.cl']
        classes = TestTypeChecker.compiler.parse_fileset(fileset)
        sa = symantic_analyzer.TypeChecker(classes)
        
        with pytest.raises(symantic_analyzer.TypeCheckingException):
            sa.type_check()

    def test_case3(self):
        fileset = ['resources/synthetic/example3.cl']
        classes = TestTypeChecker.compiler.parse_fileset(fileset)
        sa = symantic_analyzer.TypeChecker(classes)
        sa.type_check()

    def test_case4(self):
        fileset = ['resources/examples/book_list.cl']
        classes = TestTypeChecker.compiler.parse_fileset(fileset)
        sa = symantic_analyzer.TypeChecker(classes)
        sa.type_check()


    def type_check(self, fileset):
        classes = TestTypeChecker.compiler.parse_fileset(fileset)
        print('No of classes : ', len(classes))
        sa = symantic_analyzer.TypeChecker(classes)
        sa.type_check()

if __name__ == '__main__':
    ttc = TestTypeChecker()
    ttc.type_check(sys.argv[1:])
    
