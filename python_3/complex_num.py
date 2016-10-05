import numbers


class ComplexNumber:
    def __init__(self, real, imaginary=0):
        if not isinstance(real, numbers.Number) or not isinstance(imaginary, numbers.Number):
            raise ValueError
        self.re = real
        self.im = imaginary

    def __add__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        re = self.re + other.re
        im = self.im + other.im
        return ComplexNumber(re, im)

    def __sub__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        re = self.re - other.re
        im = self.im - other.im
        return ComplexNumber(re, im)

    def __mul__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        re = self.re * other.re - self.im * other.im
        im = self.re * other.im + self.im * other.re
        return ComplexNumber(re, im)

    def __truediv__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        if other.re == other.im == 0:
            raise ZeroDivisionError
        re = (self.re * other.re + self.im * other.im) / (other.re ** 2 + other.im ** 2)
        im = (-self.re * other.im + self.im * other.re) / (other.re ** 2 + other.im ** 2)
        return ComplexNumber(re, im)

    __radd__ = __add__

    def __rsub__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        re = other.re - self.re
        im = other.im - self.im
        return ComplexNumber(re, im)

    __rmul__ = __mul__

    def __rtruediv__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        if self.re == self.im == 0:
            raise ZeroDivisionError
        re = (self.re * other.re + self.im * other.im) / (self.re ** 2 + self.im ** 2)
        im = (self.re * other.im - self.im * other.re) / (self.re ** 2 + self.im ** 2)
        return ComplexNumber(re, im)

    def __iadd__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        self.re = self.re + other.re
        self.im = self.im + other.im
        return self

    def __isub__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        self.re = self.re - other.re
        self.im = self.im - other.im
        return self

    def __imul__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        self.re = self.re * other.re - self.im * other.im
        self.im = self.re * other.im + self.im * other.re
        return self

    def __itruediv__(self, other):
        if not isinstance(other, ComplexNumber):
            other = ComplexNumber(other)
        if other.re == other.im == 0:
            raise ZeroDivisionError
        self.re = (self.re * other.re + self.im * other.im) / (other.re ** 2 + other.im ** 2)
        self.im = (-self.re * other.im + self.im * other.re) / (other.re ** 2 + other.im ** 2)
        return self

    def __str__(self):
        return str(self.re) + (' - ' if self.im < 0 else ' + ') + str(self.im) + 'i'

    __repr__ = __str__

