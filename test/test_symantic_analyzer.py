import cool
import cool.symantic_analyzer as symantic_analyzer


def test_symbol_table_manager(fileset):

    compiler = cool.Compiler()
    classes = compiler.parse_fileset(fileset)

    print('No of classes : ', len(classes))
    
    sa = symantic_analyzer.TypeChecker(classes)
    #sa.print_sym_table()
    sa.type_check('Book')
    sa.type_check('Article')
    sa.type_check('BookList')
    sa.type_check('Cons')
    sa.type_check('Main')
    sa.type_check('Nil')

    
if __name__ == '__main__':
    import sys
    import os.path as osp
    
    test_symbol_table_manager(sys.argv[1:])

