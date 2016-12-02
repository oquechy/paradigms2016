import operator
from unittest.mock import MagicMock

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
    p = Scope()
    n = Number(100)
    p['fst'] = n
    f = BinaryOperation(Number(10), '%', Number(3))
    g = Function([], [Number(17)])
    p['snd'] = f
    s = Scope(p)
    p['snd'] = g
    assert s['snd'] != p['snd']
    assert s['snd'] == n

    

class Number:
    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, scope):
        return self

def test_nume():
    s = Scope()
    n1 = Number(17)
    assert n1.value == 17
    assert n1.evaluate(s) == n1 



class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

def test_ref():
    s = Scope()
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
    s = Scope()
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
    s = Scope()
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
    s = Scope()
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

def test_food():
    s = Scope()
    s['foo'] = Function([], [Reference('foo')])
    f = FunctionDefinition('foo', s['foo'])
    assert f.evaluate(s) == s['foo']


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

def test_fc():
    s = Scope()
    s['foo'] = Function([], [Reference('foo')])
    f = FunctionDefinition('foo', s['foo'])
    fc = FunctionCall(f, [])
    assert fc.evaluate(s) == s['foo']


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

def test_cond():
    s = Scope()
    n = Number(0)
    c = Conditional(Number(0), [Number(1)], [Number(1), n])
    assert c.evaluate(s) == n


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope)
        print(a.value)
        return a

def test_print():
    s = Scope()
    n = Number(0)
    assert Print(n).evaluate(s) == n


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        a = int(input())
        scope[self.name] = a
        return Number(a)

def test_read():
    r = Read('a')
    r.evaluate = MagicMock(return_value=42)
    s = Scope()
    assert r.evaluate(s) == 42


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


if __name__ == '__main__':
    test()
