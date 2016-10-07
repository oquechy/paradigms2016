import model

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
        to = l.__class__.__name__
        if l.__class__.__name__ == 'Number' and r.__class__.__name__ == 'Number':
            return model.BinaryOperation(l, bo.op, r).evaluate(s)
        elif (bo.op == '*' and (l.__class__.__name__ == 'Number' and not l.value
                               or r.__class__.__name__ == 'Number' and not r.value)
              or bo.op == '-' and l.__class__.__name__ == 'Reference' and r.__class__.__name__ == 'Reference'
                and l.name == r.name):
            return model.Number(0)
        else:
            return model.BinaryOperation(l, bo.op, r)

    def visitUnOperation(self, uo):
        expr = uo.expr.accept(self)
        s = model.Scope()
        if expr.__class__.__name__ == 'Number':
            return model.UnaryOperation(uo.op, expr).evaluate(s)
        else:
            return model.UnaryOperation(uo.op, expr)
