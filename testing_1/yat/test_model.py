import unittest
from io import StringIO
from unittest.mock import patch
from model import *


class tScope(unittest.TestCase):

    n = Number(100)
    f = BinaryOperation(Number(10), '%', Number(3))
    g = Function([], [Number(17)])

    def test_1(self):
        p = Scope()
        s = Scope(p)
        p['fst'] = self.n
        p['snd'] = self.f
        s['snd'] = self.g
        self.assertIs(s['snd'], self.g)
        self.assertIs(s['fst'], self.n)
        self.assertIs(p['fst'], self.n)
        self.assertIs(p['snd'], self.f)

    def test_2(self):
        s = Scope()
        s['fst'] = self.n
        s['snd'] = self.g
        self.assertIs(s['snd'], self.g)
        self.assertIs(s['fst'], self.n)

    def test_3(self):
        s = Scope()
        s['fst'] = self.n
        self.assertIs(s['fst'], self.n)
        s['fst'] = self.g
        self.assertIs(s['fst'], self.g)


class tNumber(unittest.TestCase):

    s = Scope()

    def test_1(self):
        n = Number(10)
        self.assertIs(n.evaluate(self.s), n)


class tFunction(unittest.TestCase):

    s = Scope()

    def test_1(self):
        n = Number(17)
        f = Function(['arg'], [Number(0), n])
        self.assertIs(f.evaluate(self.s), n)

    def test_2(self):
        f = Function([], [])
        f.evaluate(self.s)


class tFunctionDefinition(unittest.TestCase):

    s = Scope()

    def test_1(self):
        n = Number(0)
        f = Function(['arg'], [Number(17), n])
        fd = FunctionDefinition('f', f)
        self.assertIs(fd.evaluate(self.s), f)
        self.assertIs(self.s['f'], f)


class tConditional(unittest.TestCase):

    s = Scope()
    n, t, f = Number(17), Number(10), Number(0)

    def test_1(self):
        c = Conditional(self.t, [Number(1), self.n], [Number(2), Number(3)])
        self.assertIs(c.evaluate(self.s), self.n)

    def test_2(self):
        c = Conditional(self.f, [Number(1), Number(2)], [Number(3), self.n])
        self.assertIs(c.evaluate(self.s), self.n)

    def test_3(self):
        c = Conditional(self.t, [], [])
        c.evaluate(self.s)

    def test_4(self):
        c = Conditional(self.f, [])
        c.evaluate(self.s)


class tPrint(unittest.TestCase):

    s = Scope()

    @patch('sys.stdout', new_callable=StringIO)
    def test_1(self, out):
        Print(Number(-113311)).evaluate(self.s)
        self.assertEqual(out.getvalue(), '-113311\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_2(self, out):
        Print(Number(0)).evaluate(self.s)
        self.assertEqual(out.getvalue(), '0\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_3(self, out):
        Print(Number(113311)).evaluate(self.s)
        self.assertEqual(out.getvalue(), '113311\n')


class tRead(unittest.TestCase):

    s = Scope()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin', new=StringIO('-113311'))
    def test_1(self, out):
        r = Read('n').evaluate(self.s)
        Print(r).evaluate(self.s)
        self.assertEqual(out.getvalue(), '-113311\n')
        self.assertEqual(self.s['n'], r)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin', new=StringIO('0'))
    def test_2(self, out):
        r = Read('n').evaluate(self.s)
        Print(r.evaluate(self.s)).evaluate(self.s)
        self.assertEqual(out.getvalue(), '0\n')
        self.assertEqual(self.s['n'], r)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin', new=StringIO('113311'))
    def test_3(self, out):
        r = Read('n').evaluate(self.s)
        Print(r.evaluate(self.s)).evaluate(self.s)
        self.assertEqual(out.getvalue(), '113311\n')
        self.assertEqual(self.s['n'], r)


class tReference(unittest.TestCase):

    s = Scope()
    x, y, z = Number(1), Number(2), Number(3)

    def test_1(self):
        self.s['fst'], self.s['snd'], self.s['trd'] = self.x, self.y, self.z
        r1, r2, r3 = Reference('fst'), Reference('snd'), Reference('trd')
        self.assertIs(r1.evaluate(self.s), self.x)
        self.assertIs(r2.evaluate(self.s), self.y)
        self.assertIs(r3.evaluate(self.s), self.z)


class tFunctionCall(unittest.TestCase):

    s = Scope()
    n = Number(17)
    s['n'] = n

    def test_1(self):
        f = Function(['arg', 'brg'], [Reference('arg'), Reference('brg'), self.n])
        fd = FunctionDefinition('f', f)
        fc = FunctionCall(fd, [Number(1), Number(2)])
        self.assertIs(fc.evaluate(self.s), self.n)

    def test_2(self):
        f = Function([], [Reference('n')])
        fd = FunctionDefinition('f', f)
        fc = FunctionCall(fd, [])
        self.assertEqual(fc.evaluate(self.s), self.n)

    def test_3(self):
        f = Function([], [])
        fd = FunctionDefinition('f', f)
        FunctionCall(fd, []).evaluate(self.s)


class tBinaryOperation(unittest.TestCase):

    s = Scope()
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv, '%': operator.mod,
           '==': operator.eq, '!=': operator.ne, '<': operator.lt, '>': operator.gt, '<=': operator.le,
           '>=': operator.ge, '&&':  lambda x, y: 1 if x and y else 0, '||': lambda x, y: 1 if x or y else 0}

    def test_1(self):
        for i in range(-10, 10):
            for j in range(-10, 10):
                for ys, ps in self.ops.items():
                    if j != 0 or ys != '/' and ys != '%':
                        with patch("sys.stdout", new_callable=StringIO) as out:
                            Print(BinaryOperation(Number(i), ys, Number(j)).evaluate(self.s)).evaluate(self.s)
                            self.assertEqual(out.getvalue(), str(int(ps(i, j))) + '\n', str(i) + ' ' + ys + ' ' + str(j))


class UnaryOperationTest(unittest.TestCase):

    s = Scope()
    ops = {'-': '-', '!': 'not '}

    def test_1(self):
        for i in range(-10, 10):
            for ys, ps in self.ops.items():
                with patch("sys.stdout", new_callable=StringIO) as out:
                    Print(UnaryOperation(ys, Number(i)).evaluate(self.s)).evaluate(self.s)
                    self.assertEqual(out.getvalue(), str(eval('int(' + ps + str(i) + ')')) + '\n')


if __name__ == '__main__':
    unittest.main()
