import operator

class Scope(object):
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        if self.parent:
            return self.parent[item]
        else:
            raise Exception

    def __setitem__(self, key, value):
        self.dict[key] = value

def test_scope():
    Scope p
    n = Number(100)
    p['fst'] = n
    f = BinaryOperation(Number(10), '%', Number(3)
    g = Function([], [Number(17)])
    p['snd'] = f
    Scope s(p)
    p['snd'] = g
    assert s['snd'] != p['snd']
    assert s['snd'] == n

    

class Number:
    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, scope):
        return self

def test_nume():
    Scope s
    n1 = Number(17)
    assert n1.value == 17
    assert n1.evaluate(s) == n1 



class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

def test_ref():
    Scope s
    n1 = Number(1)
    s['tru'] = n1
    r = Reference('tru')
    assert r.evaluate(s) == n1


class UnaryOperation:
    ops = {"-": operator.neg,
            "!":operator.not_}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope).value
        return Number(self.ops[self.op](a))

def test_uo():
    Scope s
    uo = UnaryOperation("!", Number(5))
    assert uo.evaluate(s) == 0
    
    
class BinaryOperation:
    ops = {"+": operator.add,
            "-":operator.sub,
            "*":operator.mul,
            "/":operator.floordiv,
            "%":operator.mod,
            "==":operator.is_,
            "!=":operator.is_not,
            "<":operator.lt,
            ">":operator.gt,
            "<=":operator.le,
            ">=":operator.ge,
            "&&":lambda x, y: bool(x and y),
            "||":lambda x, y: bool(x or y)}

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope).value
        r = self.rhs.evaluate(scope).value
        return Number(self.ops[self.op](l, r))

def test_bo():
    Scope s
    bo = BinaryOperation(Number(0), '+', UnaryOperation('!', Number(0)))
    assert bo.evaluate(s) == 1


class Function:
    def __init__(self, args, body):
        self.body = body
        self.args = args

    def evaluate(self, scope):
        last = Number(0)
        for x in self.body:
            last = x.evaluate(scope)
        return last

def test_foo():
    Scope s
    n = Number(17)
    f = Function([], [n])
    assert f.evaluate(s) == n


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.func = function

    def evaluate(self, scope):
        scope[self.name] = self.func
        return self.func


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.args = args
        self.fun_expr = fun_expr

    def evaluate(self, scope):
        func = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        results = [x.evaluate(scope) for x in self.args]
        for i, x in enumerate(func.args):
            call_scope[x] = results[i]
        return func.evaluate(call_scope)


class Conditional:
    def __init__(self, condition, if_true, if_false = None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        val = self.condition.evaluate(scope)
        if val and self.if_true:
            body = self.if_true
        elif self.if_false:
            body = self.if_false
        else:
            body = []
        res = None
        for stmt in body:
            res = stmt.evaluate(scope)
        return res


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope)
        print(a.value)
        return a


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        a = int(input())
        scope[self.name] = a
        return Number(a)


def test():
    #Example
    parent = Scope()
    parent["bar"] = Number(10)
    scope = Scope(parent)
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'), '+', Reference('world')))])
   # assert type(FunctionCall(FunctionDefinition('foo', parent['foo']),
    #             [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)) == Number
    assert scope["bar"].value == 10
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    #assert type(scope["bar"]) == Number

    assert BinaryOperation(Number(5), "&&", Number(0)).evaluate(scope).value == 0
    assert BinaryOperation(Number(5), "&&", Number(-2)).evaluate(scope).value == 1
    assert UnaryOperation("!", Number(5)).evaluate(scope).value == 0
    p = Scope()
    p['Number(0)'] = UnaryOperation('-', BinaryOperation(Number(10), '%', Number(3))).evaluate(p)
    p['func'] = Function(['mama', 'papa'], [Read('me'),
                                            Conditional(BinaryOperation(BinaryOperation(Reference('mama'),
                                                                                        '+', Reference('papa')),
                                                                        '==',
                                                                        Reference('me')),
                                                        [Print(Number(1))],
                                                        [Print(Number(0))])])
    # print('@', p['Number(0)'].value)
    # print(Print(Reference('Number(0)')).evaluate(p), Print(Reference('Number(0)')).evaluate(p).value)
    BinaryOperation(Print(Reference('Number(0)')), '==', Number(-1)).evaluate(p)
    s = Scope(p)
    s['foo'] = Function([], [Reference('foo')])
    s['!!!'] = Function([], [Number(17)])
    s['foo1'] = Function([], [Reference('foo')])
    s['0'] = Function(['1', '2'], [Read('f'), Print(Reference('f')), Conditional(Reference('f'),
                                                                                 [Reference('1')], [Reference('0')])])
    s['Number(0)'] = Conditional(Number(1),
                                 [FunctionDefinition('foo', s['foo'])],
                                 FunctionDefinition('func', s['func'])).evaluate(s)
    s['num'] = Number(17)
    s['tru'] = Number(1)
    s['flse'] = Number(0)
    assert s['Number(0)'] == s['foo']
    # print('start')
    assert Print(FunctionCall(FunctionDefinition('-', s['!!!']), [])).evaluate(s) == 2
    assert Print(FunctionCall(FunctionDefinition('ty', s['func']),
                       [Number(1), FunctionCall(FunctionDefinition('-', s['!!!']), [])])).evaluate(s) == -1

    assert Print(BinaryOperation(FunctionCall(FunctionDefinition('ty', s['func']),
                                       [Number(1),
                                       FunctionCall(FunctionDefinition('-', s['!!!']), [])]),
                          '==',
                          Number(1))).evaluate(s) == 17
    Print(Reference('Number(0)')).evaluate(p) 
    Print(BinaryOperation(Reference('Number(0)'), '+', UnaryOperation('!', Number(0)))).evaluate(p)
    Print(Conditional(Number(0), [Number(1)], [Number(1), Number(0)])).evaluate(s)
    Print(BinaryOperation(Conditional(Conditional(Number(0),
                                                  [Number(1)],
                                                  [Number(1), Number(0)]),
                                      [Number(7)], [Number(8)]),
                          '-', Number(0))).evaluate(s)
    Print(BinaryOperation(Print(Read('uuu')), '*',
                          FunctionCall(FunctionDefinition('foo', s['func']), [Number(0), Number(0)]))).evaluate(s)
    Print(BinaryOperation(Number(1), '/', Number(2))).evaluate(s)
    Print(BinaryOperation(FunctionCall(FunctionDefinition('0', s['0']), [Reference('tru'), Reference('flse')]),
                          '&&',
                          Number(1))).evaluate(s)


if __name__ == '__main__':
    test()
