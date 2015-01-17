# Base node
class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        """
        default implementation that visit the subnodes in the order
        they are stored in self_field
        """
        class_name = self.__class__.__name__
        visit = getattr(visitor, 'visit_' + class_name)
        if visit(self):
            for f in self._fields:
                field = getattr(self, f)
                if field:
                    if isinstance(field, list):
                        for elem in field:
                            if isinstance(elem, SourceElement):
                                elem.accept(visitor)
                    elif isinstance(field, SourceElement):
                        field.accept(visitor)
        getattr(visitor, 'leave_' + class_name)(self)

    def type_check(self, visitor):
        """
        default implementation that visit the subnodes in the order
        they are stored in self_field
        """
        class_name = self.__class__.__name__
        visit = getattr(visitor, 'visit_' + class_name)
        typeid = None
        if visit(self):
            typeid = getattr(visitor, 'typeof_' + class_name)(self)
        getattr(visitor, 'leave_' + class_name)(self)
        return typeid

class ClassDefinition(SourceElement):

    def __init__(self, name, base_class, features):
        super(ClassDefinition, self).__init__()
        self._fields = ['variables', 'methods']

        self.name = name
        self.base_class = base_class  #this is a typeid
        self.variables = []
        self.methods = []
        
        for feature in features:
            if isinstance(feature, MethodDefinition):
                self.methods.append(feature)
            else:
                self.variables.append(feature)

class MethodDefinition(SourceElement):

    def __init__(self, name, formal_args, return_type, body):
        super(MethodDefinition, self).__init__()
        self._fields = ['formal_args', 'body']

        self.name = name
        self.formal_args = formal_args
        self.return_type = return_type
        self.body = body

    def get_signature(self):
        return ([f.typeid for f in self.formal_args],
                self.return_type)
        
class VariableDefinition(SourceElement):

    def __init__(self, var_decl, var_init):
        super(VariableDefinition, self).__init__()
        self._fields = ['var_decl', 'var_init']

        self.var_decl = var_decl
        self.var_init = var_init

class VariableDeclaration(SourceElement):

    def __init__(self, name, typeid):
        super(VariableDeclaration, self).__init__()
        self._fields = []

        self.name = name
        self.typeid = typeid
        
class Expression(SourceElement):
    
    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []

class Assignment(Expression):
    
    def __init__(self, lhs, expr):
        super(Assignment, self).__init__()
        self._fields = ['expr']

        self.lhs = lhs
        self.expr = expr

class MethodInvoke(Expression):
    
    def __init__(self, expr, at_type, name, arguments):
        super(MethodInvoke, self).__init__()
        self._fields = ['expr', 'arguments']

        self.expr = expr #left hand side of invokation
        self.at_type = at_type #this is for typecasting
        self.name = name #the method name
        self.arguments = arguments

class IfThenElse(Expression):

    def __init__(self, condition, ifbody, elsebody):
        super(IfThenElse, self).__init__()
        self._fields = ['condition', 'ifbody', 'elsebody']

        self.condition = condition
        self.ifbody = ifbody
        self.elsebody = elsebody

class WhileLoop(Expression):

    def __init__(self, condition, loopbody):
        super(WhileLoop, self).__init__()
        self._fields = ['condition', 'loopbody']

        self.condition = condition
        self.loopbody = loopbody

class BlockStatement(Expression):
    ''' of the form {[expr;]+}'''

    def __init__(self, statements):
        super(BlockStatement, self).__init__()
        self._fields = ['statements']

        self.statements = statements

class LetExpression(Expression):

    def __init__(self, var_list, expr):
        super(LetExpression, self).__init__()
        self._fields = ['var_list', 'expr']

        self.var_list = var_list
        self.expr = expr

class CaseExpression(Expression):

    def __init__(self, expr, statements):
        super(CaseExpression, self).__init__()
        self._fields = ['expr', 'statements']

        self.expr = expr
        self.statements = statements
        
class CaseStatement(Expression):

    def __init__(self, var_decl, expr):
        super(CaseStatement, self).__init__()
        self._fields = ['var_decl', 'expr']

        self.var_decl = var_decl
        self.expr = expr

class NewStatement(Expression):
    
    def __init__(self, typeid):
        super(NewStatement, self).__init__()
        self._fields = []
        
        self.typeid = typeid
        
class IsVoidExpression(Expression):
    
    def __init__(self, expr):
        super(IsVoidExpression, self).__init__()
        self._fields = ['expr']
        
        self.expr = expr
        
class ComplementExpression(Expression):
    
    def __init__(self, isbool, expr):
        super(ComplementExpression, self).__init__()
        self._fields = ['expr']
        
        self.isbool = isbool #int or bool only, true if bool
        self.expr = expr

class InBracketsExpression(Expression):
    ''' of the form (expr)'''

    def __init__(self, expr):
        super(InBracketsExpression, self).__init__()
        self._fields = ['expr']
        
        self.expr = expr
        
class BinaryOperationExpression(Expression):
    
    def __init__(self, binop, expr1, expr2):
        super(BinaryOperationExpression, self).__init__()
        self._fields = ['expr1', 'expr2']
        
        self.binop = binop
        self.expr1 = expr1
        self.expr2 = expr2
        
class ObjectIdExpression(Expression):
    
    def __init__(self, name):
        super(ObjectIdExpression, self).__init__()
        self._fields = []
        
        self.name = name
        
class NumberExpression(Expression):
    
    def __init__(self, value):
        super(NumberExpression, self).__init__()
        self._fields = []
        
        self.value = value
        
class BooleanExpression(Expression):
    
    def __init__(self, value):
        super(BooleanExpression, self).__init__()
        self._fields = []

        self.value = value
        
class StringExpression(Expression):
    
    def __init__(self, value):
        super(StringExpression, self).__init__()
        self._fields = []
        
        self.value = value


