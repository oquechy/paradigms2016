import model
import printer

class ConstantFolder:
    def visit(self, tree):
        return tree.accept(self)

    def visitNumber(self, n):
        return n

    def visitFunDefinition(self, fd):
        return model.FunctionDefinition(fd.name, fd.function.accept(self))

    def visitFunction(self, f):
        return model.Function(f.args, [exp.accept(self) for exp in f.body])

    def visitConditional(self, c):
        return model.Conditional(c.cond.accept(self), [e.accept(self) for e in c.t], [e.accept(self) for e in c.f])

    def visitPrint(self, p):
        return model.Print(p.expr.accept(self))

    def visitRead(self, r):
        return r

    def visitReference(self, r):
        return r

    def visitFunCall(self, fc):
        return model.FunctionCall(fc.fun_expr.accept(self), [arg.accept(self) for arg in fc.args])

    def visitBinOperation(self, bo):
        l, r = bo.l.accept(self), bo.r.accept(self)
        s = model.Scope()
        # print('@', type(l))
        if type(l) is model.Number and type(r) is model.Number:
            return model.BinaryOperation(l, bo.op, r).evaluate(s)
        elif (bo.op == '*' and (type(l) is model.Number and not l.value
                               or type(r) is model.Number and not r.value)
              or bo.op == '-' and type(l) is model.Reference and type(r) is model.Reference
                and l.name == r.name):
            return model.Number(0)
        else:
            return model.BinaryOperation(l, bo.op, r)

    def visitUnOperation(self, uo):
        expr = uo.expr.accept(self)
        s = model.Scope()
        if type(expr) is model.Number:
            return model.UnaryOperation(uo.op, expr).evaluate(s)
        else:
            return model.UnaryOperation(uo.op, expr)


def my_tests():
    def test_trash_func():
        scope = model.Scope()
        model.FunctionDefinition('foo',
                                 model.Function(['x'], [
                                     model.FunctionDefinition('bar', model.Function([], [model.Read('l'),
                                                                                         model.BinaryOperation(model.Reference('l'), '%',
                                                                                                               model.Reference('x'))]))])).evaluate(scope)
        model.Print(model.FunctionCall(model.FunctionCall(model.Reference('foo'), [model.Number(5)]), [])).evaluate(scope)

    test_trash_func()
    '''p = model.Scope()
    p['Number(0)'] = model.UnaryOperation('-', model.BinaryOperation(model.Number(10), '%', model.Number(3))).evaluate(p)
    p['func'] = model.Function(['mama', 'papa'], [model.Read('me'),
                                                  model.Conditional(model.BinaryOperation(model.BinaryOperation(model.Reference('mama'),
                                                                                        '+', model.Reference('papa')),
                                                                        '==',
                                                                                          model.Reference('me')),
                                                        [model.Print(model.Number(1))],
                                                        [model.Print(model.Number(0))])])
    bo = model.BinaryOperation(model.Print(model.Reference('Number(0)')), '==', model.Number(-1))
    s = model.Scope(p)
    s['foo'] = model.Function([], [model.Reference('foo')])
    s['!!!'] = model.Function([], [model.Number(17)])
    s['foo1'] = model.Function([], [model.Reference('foo')])
    s['0'] = model.Function(['1', '2'], [model.Read('f'), model.Print(model.Reference('f')), model.Conditional(model.Reference('f'),
                                                                                 [model.Reference('1')], [model.Reference('0')])])
    s['Number(0)'] = model.Conditional(model.Number(1),
                                 [model.FunctionDefinition('foo', s['foo'])],
                                       model.FunctionDefinition('func', s['func'])).evaluate(s)
    s['num'] = model.Conditional(model.Number(1), [model.Print(model.Reference('x')), model.Read('d'), model.Number(0)])
    s['tru'] = model.Number(1)
    s['flse'] = model.Number(0)
    # printer.PrettyPrinter.visit(printerr, s['func'])
    pretty = printer.PrettyPrinter()
    printerr = printer.PrettyPrinter()
    pretty.visit(model.Print(model.Conditional(model.Number(0), [model.Number(1)], [model.Number(1), model.Number(0)])))
    printerr.visit(model.FunctionDefinition('func', s['func']))
    printerr.visit(p['Number(0)'])
    printerr.visit(model.Conditional(model.Number(10), [model.Print(model.Number(10))], []))
    printerr.visit(model.FunctionDefinition('num0', s['Number(0)']))
    printerr.visit(model.FunctionDefinition('f00', s['foo']))
    printerr.visit(model.FunctionDefinition('!!!', s['!!!']))
    printerr.visit(model.Reference('foo1'))
    printerr.visit(model.Reference('0'))
    printerr.visit(s['num'])
    printerr.visit(s['tru'])
    printerr.visit(s['flse'])
    pretty.visit(model.Print(model.FunctionCall(model.FunctionDefinition('-', s['!!!']), [])))
    pretty.visit(model.Print(model.FunctionCall(model.FunctionDefinition('ty', s['func']),
                       [model.Number(1), model.FunctionCall(model.FunctionDefinition('-', s['!!!']), [])])))

    pretty.visit(model.BinaryOperation(model.FunctionCall(model.FunctionDefinition('ty', s['func']),
                                       [model.Number(1),
                                        model.FunctionCall(model.FunctionDefinition('-', s['!!!']), [])]),
                                 '==',
                                       model.Number(1)))
    pretty.visit(model.Reference('Number(0)'))
    pretty.visit(model.Print(model.BinaryOperation(model.Reference('Number(0)'), '+', model.UnaryOperation('!', model.Number(0)))))
    pretty.visit(model.Print(model.BinaryOperation(model.Conditional(model.Conditional(model.Number(0),
                                                  [model.Number(1)],
                                                  [model.Number(1), model.Number(0)]),
                                      [model.Number(7)], [model.Number(8)]),
                          '-', model.Number(0))))
    pretty.visit(model.Print(model.BinaryOperation(model.Print(model.Read('uuu')), '*',
                                                   model.FunctionCall(model.FunctionDefinition('foo', s['func']), [model.Number(0), model.Number(0)]))))
    pretty.visit(model.BinaryOperation(model.Number(1), '/', model.Number(2)))
    pretty.visit(model.Print(model.BinaryOperation(model.FunctionCall(model.FunctionDefinition('0', s['0']), [model.Reference('tru'), model.Reference('flse')]),
                          '&&',
                                                   model.Number(1))))

    fold = ConstantFolder()
    printerr.visit(model.Number(0))
    printerr.visit(fold.visit(model.Number(0)))
    bo1 = model.BinaryOperation(model.Number(0), '*', model.Reference('i'))
    printerr.visit(bo1)
    printerr.visit(fold.visit(bo1))
    bo2 = model.BinaryOperation(model.FunctionCall(model.Reference('foo'),
                                            [model.BinaryOperation(model.Reference('o'), '*', model.Number(0)), model.Number(10), model.Number(100)]),
                          '*',
                                model.Reference('i'))
    bo3 = model.Conditional(model.BinaryOperation(model.BinaryOperation(model.BinaryOperation(model.Reference('i'), '-', model.Reference('i')),
                                                      '&&',
                                                                  model.Number(9)),
                                      '==',
                                            model.Reference('x')), [model.Number(0), bo1], [bo1, bo1])
    printerr.visit(bo2)
    printerr.visit(fold.visit(bo2))
    printerr.visit(bo3)
    printerr.visit(fold.visit(bo3))
    func = model.FunctionDefinition('hard', model.Function(['a', 'b', 'c', 'd'], [model.UnaryOperation('-', model.Number(0)),
                                                                                  model.BinaryOperation(model.Reference('a'), '*', model.Number(1)),
                                                                                  model.Number(0),
                                                                                  model.Conditional(model.Number(0), [], [bo2])]))
    funcc = model.FunctionCall(func, [model.Number(1), bo1, bo3, bo2])
    printerr.visit(func)
    printerr.visit(fold.visit(func))
    printerr.visit(funcc)
    printerr.visit(fold.visit(funcc))
    '''


if __name__ == '__main__':
    my_tests()