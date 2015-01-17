from .model import ClassDefinition

class TypeCheckingException(Exception):
    pass

class MultipleDefinitionException(TypeCheckingException):
    
    def __init__(self, typeid):
        self._typeid = typeid
        
    def __str__(self):
        return 'Multiple definitions for class : ' + self._typeid
    
class MultipleDeclarationException(TypeCheckingException):
    pass

class UnknownTypeException(TypeCheckingException):
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

    def get_parent(self, typeid):
        return self._dict.get(typeid, None)

    def is_parent(self, parent_typeid, child_typeid):

        if parent_typeid == child_typeid:
            return False
        else:
            _typeid = child_typeid
            while _typeid is not None:
                if self._dict[_typeid] == parent_typeid:
                    return True
                else:
                    _typeid = self._dict[_typeid]
            return False
                
    def common_ancestor(self, _list):

        if len(_list) == 1:
            return _list[0]
        else:
            c = _list[0]
            for l in _list[1:]:
                if c != l:
                    c = self._common_ancestor_helper(self._stackup(c),
                                                     self._stackup(l))
            return c

    def _common_ancestor_helper(self, l1, l2):

        max_len = len(min(l1, l2))
        for i in range(1, max_len+1):
            if l1[-i] != l2[-i]:
                return l1[-i+1]
        return min(l1, l2)[0]

    def _stackup(self, typeid):

        def _stackup_helper(_dict, _typeid):
            '''
            Could go into infinite loop if
            their is a circular dependency
            '''
            while True:
                if _typeid is None:
                    break
                else:
                    yield _typeid
                    _typeid = _dict[_typeid]

        return [t for t in _stackup_helper(self._dict, typeid)]


class SymanticAnalyzer:
        
    def __init__(self, ast):

        self._ast = ast
        self._scope_stack = list()
        self._init_sym_table()
        self._curr_class = None
        
    def _init_sym_table(self):

        self._sym_table = SymbolTable()
        
        #TODO: parse basic.cl instead of statically loading symbol table
        #self._sym_table.add_type('Object', None)
        #self._sym_table.add_type('Int', 'Object')
        #self._sym_table.add_type('String', 'Object')
        #self._sym_table.add_type('Bool', 'Object')
        #self._sym_table.add_type('IO', 'Object')
        
        for _cls in self._ast:
            if isinstance(_cls, ClassDefinition):
                base_class = 'Object' if _cls.base_class is None \
                             else _cls.base_class

                try:
                    self._sym_table.add_type(_cls.name, base_class)
                except MultipleDefinitionException as err:
                    print(err)

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
        #CODE SMELLS: not sure if this is correct
        if objectid == 'self':
            #return self._curr_class
            return 'SELF_TYPE'
        else:
            for scope in reversed(self._scope_stack):
                if objectid in scope.keys():
                    return scope[objectid]

    def print_sym_table(self):
        self._sym_table._print_dict()

    def check(self):
        for _cls in self._ast:
            self._curr_class = _cls.name
            _cls.accept(self)

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
            var_decl.typeid))

        if not self._sym_table.isdefined(var_decl.typeid):
            raise ClassNotFoundException(var_decl.typeid)
        else:
            self._add_object(var_decl.name, var_decl.typeid)
        
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


class TypeChecker(SymanticAnalyzer):

    def __init__(self, ast):
        super(TypeChecker, self).__init__(ast)

    def common_ansestor(self, _list):
        return self._sym_table.common_ansestor(_list)

    def is_parent(self, parent_typeid, child_typeid):
        self._sym_table.is_parent(parent_typeid, child_typeid)
        
    def _get_method_sign_helper(self, _cls, mthd):

        if _cls is not None:
            if any(m.name == mthd for m in _cls.methods):
                for m in _cls.methods:
                    if m.name == mthd:
                        return m.get_signature()
            else:
                parent_typeid = self._sym_table.get_parent(_cls)
                return self._get_method_sign_helper(parent_typeid, mthd)
        
    def get_method_sign(self, typeid, mthd):
        
        for _cls in self._ast:
            if _cls.name == typeid:
                return self._get_method_sign_helper(_cls, mthd)

    def type_check_class(self, class_name):
        for _cls in self._ast:
            if _cls.name == class_name:
                _cls.type_check(self)
        
    def type_check(self):
        ''' The main typechecker class'''
        for _cls in self._ast:
            _cls.type_check(self)

    def typeof_ClassDefinition(self, arg):

        for variable in arg.variables:
            variable.type_check(self)

        for method in arg.methods:
            method.type_check(self)

        return arg.name

    def typeof_MethodDefinition(self, arg):
        
        if arg.body.type_check(self) == arg.return_type:
            return arg.return_type
        else:
            raise TypeCheckingException(arg)

    def typeof_VariableDefinition(self, arg):
        type_var = arg.var_decl.type_check(self)
        type_expr = arg.var_init.type_check(self)
        
        if self.is_parent(type_var, type_expr):
            return type_var
        else:
            raise TypeCheckingException(arg)
            
    def typeof_VariableDeclaration(self, arg):
        #CODE SMELLS
        if arg.typeid == 'SELF_TYPE':
            return self._curr_class
        else:
            return arg.typeid

    def typeof_Assignment(self, arg):
        type_lhs = self._get_type(arg.lhs)
        type_expr = arg.expr.type_check(self)

        if type_lhs == type_expr:
            return type_lhs
        else:
            TypeCheckingException(arg)

    def typeof_MethodInvoke(self, arg):
        '''
        checks if the method signature matches
        the method definition
        '''
        type_expr_list = []

        for method_arg in arg.arguments:
            type_expr_list.append(method_arg.type_check(self))

        #typecheck lefthand side expression
        if arg.expr is not None:
            type_lhs_expr = arg.expr.type_check(self)

            if arg.at_type is not None:
                if self.is_parent(arg.at_type, type_lhs_expr):
                    type_lhs_expr = arg.at_type
                else:
                    raise TypeCheckingException(arg)
        else:
            type_lhs_expr = self._curr_class
        
        #get the function signature
        mthd_sign = self.get_method_sign(type_lhs_expr, arg.name)

        if mthd_sign is None:
            raise TypeCheckingException('could not find method' + arg)

        if len(mthd_sign[0]) != len(type_expr_list):
            raise TypeCheckingException('Method number of arguments do not match' + arg)
        for i in range(0, len(type_expr_list)):
            type_actl_arg = type_expr_list[i]
            type_frml_arg = mthd_sign[0][i]

            if not self.isparent(type_frml_arg, type_actl_arg):
                raise TypeCheckingException('Method formal argument type do not match actual argument type'.format(type_actl_arg, type_frml_arg))
            
        #method signature get return type
        if mthd_sign[1] == 'SELF_TYPE':
            return type_lhs_expr
        else:
            return mthd_sign[1]

    def typeof_IfThenElse(self, arg):
        if arg.condition.type_check(self) != 'Bool':
            raise TypeCheckingException

        type_if = arg.ifbody.type_check(self)
        type_else = arg.elsebody.type_check(self)
        return self.common_ansestor([type_if, type_else])

    def typeof_WhileLoop(self, arg):
        if arg.condition.type_check(self) != 'Bool':
            raise TypeCheckingException
        arg.loopbody.type_check(self)
        return 'Object'

    def typeof_BlockStatement(self, arg):
        for stat in arg.statements[:-1]:
            stat.type_check(self)
        return stat.type_check(self)

    def typeof_LetExpression(self, arg):
        return expr.type_check(self)

    def typeof_CaseExpression(self, arg):
        #TODO: should arg.expr match that of case statements
        arg.expr.type_check(self)
        type_expr_list = []

        for stat in arg.statements:
            type_expr_list.append(stat.type_check(self))

        return self.common_ansestor(type_expr_list)

    def typeof_CaseStatement(self, arg):
        return arg.expr.type_check(self)

    def typeof_NewStatement(self, arg):
        #TODO: this is incorrect if arg.typeid is SELF_TYPE
        if arg.typeid == 'SELF_TYPE':
            return self._curr_class
        else:
            return arg.typeid

    def typeof_IsVoidExpression(self, arg):
        arg.type_check(self)
        return 'Bool'

    def typeof_ComplementExpression(self, arg):
        typeof_expr = arg.expr.type_check(self)

        if arg.isbool:
            if typeof_expr == 'Bool':
                return 'Bool'
            else:
                raise TypeCheckingException(arg)
        else:
            if typeof_expr == 'Int':
                return 'Int'
            else:
                raise TypeCheckingException(arg)

    def typeof_InBracketsExpression(self, arg):
        return arg.expr.type_check(self)

    def typeof_BinaryOperationExpression(self, arg):

        typeof_expr1 = arg.expr1.type_check(self)
        typeof_expr2 = arg.expr2.type_check(self)

        if arg.binop in ['+', '-', '*', '/']:
            if typeof_expr1 == 'Int' and \
               typeof_expr2 == 'Int':
                return 'Int'
            else:
                raise TypeCheckingException(arg)
        elif arg.binop in ['<', '<=']:
            if typeof_expr1 == 'Int' and \
               typeof_expr2 == 'Int':
                return 'Bool'
            else:
                raise BinopTypeCheckingException(arg)
        else: #elif arg.binop == '=':
            valid_types = ['Int', 'Bool', 'String']
            if typeof_expr1 in valid_types and \
               typeof_expr2 in valid_types and \
               typeof_expr1 == typeof_expr2:
                return 'Bool'
            else:
                #TODO: this does not look right
                #return self.common_ansestor([typeof_expr1, typeof_expr2])
                raise NotImplementedError()
                
    def typeof_ObjectIdExpression(self, arg):
        return self._get_type(arg.name)

    def typeof_NumberExpression(self, arg):
        return 'Int'

    def typeof_BooleanExpression(self, arg):
        return 'Bool'

    def typeof_StringExpression(self, arg):
        return 'String'


    
