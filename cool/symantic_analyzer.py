from .model import ClassDefinition

class MultipleDefinitionException(Exception):
    
    def __init__(self, typeid):
        self._typeid = typeid
        
    def __str__(self):
        return 'Multiple definitions for class : ' + self._typeid
    
class MultipleDeclarationException(Exception):
    pass

class UnknownTypeException(Exception):
    pass

    
class SymbolTable:

    def __init__(self):
        self._dict = dict()

    def add_type(self, typeid, parentid):
        
        if not self.isdefined(typeid):
            self._dict[typeid] = parentid
        else:
            raise MultipleDefinitionException(typeid) 

    def isdefined(self, typeid):
        return True if typeid in self._dict else False

    def _print_dict(self):
        i = 1
        for key in sorted(self._dict.keys()):
            print(i, key, self._dict[key])
            i += 1
        
class SymanticAnalyzer:
        
    def __init__(self, ast):

        self._ast = ast
        self._scope_stack = list()
        self._init_sym_table()
        
    def _init_sym_table(self):
        self._sym_table = SymbolTable()
        self._sym_table.add_type('Object', None)
        self._sym_table.add_type('Int', 'Object')
        self._sym_table.add_type('String', 'Object')
        self._sym_table.add_type('Bool', 'Object')

        for _cls in self._ast:
            if isinstance(_cls, ClassDefinition):
                base_class = 'Object' if _cls.base_class is None \
                             else _cls.base_class

                try:
                    self._sym_table.add_type(_cls.name, base_class)
                except MultipleDefinitionException as err:
                    print(err)
                    #TODO: handle the error in a better way

    def _new_scope(self):
        self._scope_stack.append(dict())

    def _pop_scope(self):
        self._scope_stack.pop()

    def _add_object(self, objectid, typeid):
        
        if not self._sym_table.isdefined(typeid):
            raise UnknownTypeException(typeid)
            
        if objectid is not self._scope_stack[-1]:
            self._scope_stack[-1][objectid] = typeid
        else:
            raise MultipleDeclarationException(objectid)

    def _isdeclared_inscope(self, objectid):
        return True if objectid in self._scope_stack[-1] else False

    def _get_type(self, objectid):
        for scope in reversed(self._scope_stack):
            if objectid in scope:
                return scope[objectid]

    def print_sym_table(self):
        self._sym_table._print_dict()

    #visitors
    def visit_ClassDefinition(self, class_def):
        print('visiting class def :', class_def.name)
        self._new_scope()
        return True
        
    def leave_ClassDefinition(self, class_def):
        print('leaving class def')
        self._pop_scope()
        
    def visit_VariableDefinition(self, var_decl):
        return True
        
    def leave_VariableDefinition(self, var_decl):
        pass

    def visit_VariableDeclaration(self, var_decl):
        print('visiting variable decl : ({0}, {1})'.format(
            var_decl.name,
            var_decl.class_name))

        if not self._sym_table.isdefined(var_decl.class_name):
            raise ClassNotFoundException(var_decl.class_name)
        else:
            self._add_object(var_decl.name, var_decl.class_name)
        
    def leave_VariableDeclaration(self, var_decl):
        print('leaving variable decl : ', var_decl)

    def visit_MethodDefinition(self, method_def):
        print('visiting method def :', method_def.name)
        self._new_scope()
        return True

    def leave_MethodDefinition(self, method_def):
        self._pop_scope()

    def visit_Expression(self, arg):
        return True

    def leave_Expression(self, arg):
        pass

    def visit_Assignment(self, arg):
        return True

    def leave_Assignment(self, arg):
        pass

    def visit_MethodInvoke(self, arg):
        return True

    def leave_MethodInvoke(self, arg):
        pass

    def visit_IfThenElse(self, arg):
        return True

    def leave_IfThenElse(self, arg):
        pass

    def visit_WhileLoop(self, arg):
        return True
        pass

    def leave_WhileLoop(self, arg):
        pass

    def visit_BlockStatement(self, arg):
        return True

    def leave_BlockStatement(self, arg):
        pass

    def visit_LetExpression(self, lef_exp):
        print('visiting let expression :')
        self._new_scope()
        return True

    def leave_LetExpression(self, arg):
        self._pop_scope()

    def visit_CaseExpression(self, arg):
        return True

    def leave_CaseExpression(self, arg):
        pass

    def visit_CaseStatement(self, arg):
        print('visiting case statement :')
        self._new_scope()
        return True

    def leave_CaseStatement(self, arg):
        self._pop_scope()

    def visit_NewStatement(self, arg):
        return True

    def leave_NewStatement(self, arg):
        pass

    def visit_IsVoidExpression(self, arg):
        return True

    def leave_IsVoidExpression(self, arg):
        pass

    def visit_ComplementExpression(self, arg):
        return True

    def leave_ComplementExpression(self, arg):
        pass

    def visit_InBracketsExpression(self, arg):
        return True

    def leave_InBracketsExpression(self, arg):
        pass

    def visit_BinaryOperationExpression(self, arg):
        return True

    def leave_BinaryOperationExpression(self, arg):
        pass

    def visit_ObjectIdExpression(self, arg):
        return True

    def leave_ObjectIdExpression(self, arg):
        pass

    def visit_NumberExpression(self, arg):
        return True

    def leave_NumberExpression(self, arg):
        pass

    def visit_BooleanExpression(self, arg):
        return True

    def leave_BooleanExpression(self, arg):
        pass

    def visit_StringExpression(self, arg):
        return True

    def leave_StringExpression(self, arg):
        pass

    def check(self):

        for _cls in self._ast:
            _cls.accept(self)
