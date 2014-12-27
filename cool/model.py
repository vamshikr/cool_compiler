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


class ClassDefinition(SourceElement):

    def __init__(self, typeid, parent_typeid, features):
        super(ClassDeclaration, self).__init__()
        self._fields = ['typeid', 'parent_typeid', 'features']

        self.typeid = typeid
        self.parent_typeid = parent_typeid
        self.features = features
        

class MethodDefinition(SourceElement):

    def __init__(self, name, formal_args, return_type, body):
        super(MethodDefinition, self).__init__()
        self._fields = ['name', 'formal_args',
                        'return_type',
                        'body']

        self.name = name
        self.formal_args = formal_args
        self.return_type = return_type
        self.body = body

class VariableDefinition(SourceElement):

    def __init__(self, var_decl, var_init):
        super(VariableDefinition, self).__init__()
        self._fields = ['var_decl', 'var_init']

        self.var_decl = var_decl
        self.var_init = var_init

class VariableDeclaration(SourceElement):

    def __init__(self, name, typeid):
        super(VariableDeclaration, self).__init__()
        self._fields = ['name', 'typeid']

        self.name = name
        self.typeid = typeid
        
class Expression(SourceElement):
    
    def __init__(self, name, typeid):
        super(Expression, self).__init__()
        self._fields = []

class Assignment(Expression):
    
    def __init__(self, objectid, expr):
        super(Assignment, self).__init__()
        self._fields = ['objectid', 'expr']

        self.objectid = objectid
        self.expr = expr


class MethodInvoke(Expression):
    
    def __init__(self, expr, typeid, objectid, arguments):
        super(MethodInvoke, self).__init__()
        self._fields = ['expr', 'typeid', 'objectid', 'arguments']

        self.expr = expr #left hand side of invokation
        self.typeid = typeid #this is for typecasting
        self.objectid = objectid #the method name
        self.arguments = arguments

    
class LocalMethodInvoke(Expression):

    def __init__(self, objectid, arguments):
        super(LocalMethodInvoke, self).__init__()
        self._fields = ['objectid', 'arguments']

        self.objectid = objectid #the method name
        self.arguments = arguments

class IfThenElse(Expression):

    def __init__(self, condition, ifstat, elsestat):
        super(IfThenElse, self).__init__()
        self._fields = ['condition', 'ifstat', 'elsestat']

        self.condition = condition
        self.ifstat = ifstat
        self.elsestat = elsestat

class WhileLoop(Expression):

    def __init__(self, condition, loopbody):
        super(WhileLoop, self).__init__()
        self._fields = ['condition', 'loopbody']

        self.condition = condition
        self.loopbody = loopbody

class BlockStatement(Expression):

    def __init__(self, statements):
        super(BlockStatement, self).__init__()
        self._fields = ['statements']

        self.statements = statements

class LetExpression(Expression):

    def __init__(self, varlist, expr):
        super(LetExpression, self).__init__()
        self._fields = ['varlist', 'expr']

        self.varlist = varlist
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
        
    def __init__(self, isbool, expr):
        super(InBracketsExpression, self).__init__()
        
        self._fields = ['expr']
        self.expr = expr
        
class BinaryOperationExpression(Expression):
    
    def __init__(self, binop, expr1, expr2):
        super(BinaryOperationExpression, self).__init__()
        
        self._fields = ['expr1', 'expr2']
        self.binop = binop
        self.expr1 = expr2
        self.expr2 = expr2
        
class ObjectIdExpression(Expression):
    
    def __init__(self, objectid):
        super(ObjectIdExpression, self).__init__()
        
        self._fields = []
        self.objectid = objectid
        
    
            
            


