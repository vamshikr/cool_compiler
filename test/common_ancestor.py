
class ObjectHierarchy:

    def __init__(self, _dict):
        self._dict = _dict

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
        #print(l1)
        #print(l2)
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

if __name__ == '__main__':
    d = {
        'IO' : 'Object',
        'App' : 'Expr',
        'Bool' : 'Object',
        'Expr' : 'IO',
        'Int' : 'Object',
        'Lambda' : 'Expr',
        'LambdaList' : 'Object',
        'LambdaListNE' : 'LambdaList',
        'LambdaListRef' : 'Object',
        'Main' : 'Term',
        'Object' : None,
        'String' : 'Object',
        'Term' : 'IO',
        'VarList' : 'IO',
        'VarListNE' : 'VarList',
        'Variable' : 'Expr',
    }

    obh = ObjectHierarchy(d)
    print(obh.common_ancestor(['VarListNE', 'Expr']))
    print(obh.common_ancestor(['Expr', 'Expr']))
    print(obh.common_ancestor(['VarListNE', 'Object']))
    print(obh.common_ancestor(['VarListNE', 'VarList']))
    print(obh.common_ancestor(['VarListNE', 'VarList', 'IO']))
    print(obh.common_ancestor(['VarListNE', 'Bool']))
    print(obh.common_ancestor(['VarListNE', 'Variable']))
    print(obh.common_ancestor(['VarListNE', 'Variable', 'Term']))
    print(obh.common_ancestor(['VarListNE', 'Variable', 'Term', 'Int']))

    