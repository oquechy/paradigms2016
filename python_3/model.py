#!/usr/bin/env python3


from collections import defaultdict


class Scope:

    def __init__(self, parent=None):
        self.father = parent
        self.dict = defaultdict(lambda: None)

    def __getitem__(self, item):
        return self.father[item] if (self.dict[item] is None and self.father) else self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number:


    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, scope):
        return self


class Function:


    def __init__(self, args, body):
        self.args = args
        self.body = body
        self.value = "function!!!"

    def evaluate(self, scope):
        res = None
        for exp in self.body:
            res = exp.evaluate(scope)
        #print('Funcn', res.value)
        return res


class FunctionDefinition:


    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:


    def __init__(self, condition, if_true, if_false=None):
        self.cond = condition
        self.t = if_true
        self.f = if_false

    def evaluate(self, scope):
        res = None
        for expr in self.f if self.cond.evaluate(scope).value == 0 else self.t:
            res = expr.evaluate(scope)
        #print('Cond', self.cond.evaluate(scope).value, 'res', res.value)
        return res


class Print:


    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        n = self.expr.evaluate(scope)
        print(n.value)
        return n


class Read:


    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:


    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        fun = self.fun_expr.evaluate(scope)
        fun_scope = Scope(scope)
        for name, value in zip(fun.args, self.args):
            fun_scope[name] = value.evaluate(scope)
        res = fun.evaluate(fun_scope)
        #print('FunCall', self.fun_expr.name, res.value)
        return res


class Reference:


    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        #print('Refec', self.name, scope[self.name].value)
        return scope[self.name]


class BinaryOperation:


    def __init__(self, lhs, op, rhs):
        self.l = lhs
        self.op = op
        self.r = rhs
        assert op in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||']

    def evaluate(self, scope):
        if self.op == '&&':
            self.op = 'and'
        elif self.op == '||':
            self.op = 'or'
        lev = str(self.l.evaluate(scope).value)
        rev = str(self.r.evaluate(scope).value)
        res = eval(lev + ' ' + self.op + ' ' + rev)
        # print('BinOP', 'l =', lev, self.op, 'r =', rev, 'res =', res)
        return Number(res)


class UnaryOperation:


    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        assert op in ['-', '+']

    def evaluate(self, scope):
        if self.op == '!':
            self.op = 'not '
        return Number(eval(self.op + str(self.expr.evaluate(scope).value)))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    #print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():

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
    assert BinaryOperation(Print(Reference('Number(0)')), '==', Number(-1)).evaluate(p)
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
    Print(FunctionCall(FunctionDefinition('-', s['!!!']), [])).evaluate(s)
    Print(FunctionCall(FunctionDefinition('ty', s['func']),
                       [Number(1), FunctionCall(FunctionDefinition('-', s['!!!']), [])])).evaluate(s)

    Print(BinaryOperation(FunctionCall(FunctionDefinition('ty', s['func']),
                                       [Number(1),
                                       FunctionCall(FunctionDefinition('-', s['!!!']), [])]),
                          '==',
                          Number(1))).evaluate(s)
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
    example()
    my_tests()
