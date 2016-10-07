def sentence(func):
    def wrapping(*args, **kwargs):
        func(*args, **kwargs)
        print(';')


class PrettyPrinter:

    def __init__(self):
        self.indent = 0

    def tab(self):
        print(' ' * self.indent, end='')

    # @sentence
    def visit(self, tree):
        tree.accept(self)
        print(';')

    def visitNumber(self, n):
        # self.tab()
        print(n.value, end='')
        return len(str(n.value))

    def visitFunDefinition(self, fd):
        # self.tab()
        print('def ' + fd.name + '(', end='')
        print(*fd.function.args, sep=', ', end='')
        print(') {')
        self.indent += 4
        for exp in fd.function.body:
            self.tab()
            self.visit(exp)
        self.indent -= 4
        self.tab()
        print('}', end='')
        return 1

    def visitConditional(self, c):
        # self.tab()
        print('if (', end='')
        self.indent += 4
        c.cond.accept(self)
        print(') {')
        for exp in c.t:
            self.tab()
            exp.accept(self)
            print()
        self.indent -= 4
        self.tab()
        print('} else {')
        self.indent += 4
        for exp in c.f:
            self.tab()
            exp.accept(self)
            print()
        self.indent -= 4
        self.tab()
        print('}', end='')
        return 1

    def visitPrint(self, p):
        #self.tab()
        print('print ', end='')
        self.indent += 6
        sz = 6 + p.expr.accept(self)
        self.indent -= 6
        return sz

    def visitRead(self, r):
        #self.tab()
        print('read ' + r.name, end='')
        return 5 + len(r.name)

    def visitReference(self, r):
        print(r.name, end='')
        return len(r.name)

    def visitFunCall(self, fc):
        fix = self.indent
        sz = fc.fun_expr.accept(self) + 1
        print('(', end='')
        self.indent = fix + sz
        for exp in fc.args[:-1]:
            sz += exp.accept(self) + 2
            print(', ', end='')
            self.indent = fix + sz
        # print(fc.args)
        if fc.args:
            sz += fc.args[-1].accept(self)
        sz += 1
        print(')', end='')
        self.indent = fix
        return sz

    def visitBinOperation(self, bo):
        print('(', end='')
        self.indent += 1
        lsz = bo.l.accept(self) + 5 + len(bo.op)
        print(') ' + bo.op + ' (', end='')
        self.indent += lsz - 1
        rsz = bo.r.accept(self) + 1
        self.indent -= lsz
        print(')', end='')
        return lsz + rsz

    def visitUnOperation(self, uo):
        print(uo.op + '(', end='')
        self.indent += 1
        sz = 3 + uo.expr.accept(self)
        self.indent -= 1
        print(')', end='')
        return sz

