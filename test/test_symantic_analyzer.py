import cool
import cool.symantic_analyzer as symantic_analyzer


def test_symbol_table_manager(fileset):

    compiler = cool.Compiler()
    classes = compiler.parse_fileset(fileset)

    print('No of classes : ', len(classes))
    
    #sa = symantic_analyzer.SymanticAnalyzer(classes)
    sa = symantic_analyzer.TypeChecker(classes)
    #sa.print_sym_table()
    #print(sa._sym_table._dict)
    sa.type_check('Book')
    #sa.check()
    
if __name__ == '__main__':
    import sys
    import os.path as osp
    
    test_symbol_table_manager(sys.argv[1:])

