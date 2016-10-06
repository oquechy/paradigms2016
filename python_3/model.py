#!/usr/bin/env python3

# Шаблон для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError

from collections import defaultdict


class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

    def __init__(self, parent=None):
        self.father = parent
        self.dict = defaultdict(lambda: None)

    def __getitem__(self, item):
        return self.father[item] if (self.dict[item] is None and self.father) else self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number:

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, scope):
        return self


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Во время вычисления функции (метод evaluate),
    все объекты тела функции вычисляются последовательно,
    и результат вычисления последнего из них
    является результатом вычисления функции.
    Список имен аргументов - список имен
    формальных параметров функции."""

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

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

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

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        n = self.expr.evaluate(scope)
        print(n.value)
        return n


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

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

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        #print('Refec', self.name, scope[self.name].value)
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

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

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

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
    print('It should print 2: ', end=' ')
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
