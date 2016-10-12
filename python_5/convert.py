import math

def conv(n, base=2):
    res = []
    while n:
        res.append(n % base)
        n //= base
    return list(reversed(res))


def dec(num, base=2):
    res = p = 0
    for n in reversed(num):
        res += n * base ** p
        p += 1
    return res


def conv_f(frac, i, base=2):
    res = []
    n = len(frac)
    a = int(frac)
    for _ in range(i):
        if not frac:
            break
        b = (frac * base) // d
        if (frac * base) // :
            res.append(1)
        else:
            res.append(0)
        a -= b * d
    return res