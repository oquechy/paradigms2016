import numpy as np
from math import log2, ceil
#from random import randint

def strassen(a, b, n):
    if n == 1:
        return a.dot(b)
    a11, a12, a21, a22 = a[:n // 2, :n // 2], a[:n // 2, n // 2:], a[n // 2:, :n // 2], a[n // 2:, n // 2:]
    b11, b12, b21, b22 = b[:n // 2, :n // 2], b[:n // 2, n // 2:], b[n // 2:, :n // 2], b[n // 2:, n // 2:]
    p1 = strassen(a11 + a22, b11 + b22, n // 2)
    p2 = strassen(a21 + a22, b11, n // 2)
    p3 = strassen(a11, b12 - b22, n // 2)
    p4 = strassen(a22, b21 - b11, n // 2)
    p5 = strassen(a11 + a12, b22, n // 2)
    p6 = strassen(a21 - a11, b11 + b12, n // 2)
    p7 = strassen(a12 - a22, b21 + b22, n // 2)
    c = np.vstack((np.hstack((p1 + p4 - p5 + p7, p3 + p5)), np.hstack((p2 + p4,p1 + p3 - p2 + p6))))
    return c


def test_strassen(n):
    n = 2 ** n
    a = np.random.randint(0, 160, (n, n))
    b = np.random.randint(0, 160, (n, n))
    c1 = strassen(a, b, n)
    c2 = a.dot(b)
    print('-' * 80)
    for row in c1:
        print(*row)
    print()
    for row in c2:
        print(*row)
    print()
    print((c1 == c2).all())
    print('-' * 80)
    return (c1 == c2).all()


def main():
    m = int(input())
    a1 = np.array([list(map(int, input().split())) for _ in range(m)])
    b1 = np.array([list(map(int, input().split())) for _ in range(m)])
    n = 2 ** ceil(log2(m))
    a = np.zeros((n, n), dtype='int')
    b = np.zeros((n, n), dtype='int')
    a[:m, :m] = a1
    b[:m, :m] = b1
    for row in strassen(a, b, n)[:m, :m]:
        print(*row)

if __name__ == '__main__':
    main()
    #for i in range(10):
    #    if not test_strassen(randint(0, 6)):
    #       print('wrong!!! (test ', i, ')')


