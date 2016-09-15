#!/usr/bin/env python


def remove_adjacent(lst):
    ans = []
    i = 0
    n = len(lst)
    while i < n:
        ans.append(lst[i])
        i += 1
        while i < n and lst[i] == lst[i - 1]:
            i += 1
    return ans


def linear_merge(lst1, lst2):
    i1 = i2 = 0
    n1 = len(lst1)
    n2 = len(lst2)
    ans = []
    while i1 < n1 and i2 < n2:
        if lst1[i1] < lst2[i2]:
            ans.append(lst1[i1])
            i1 += 1
        else:
            ans.append(lst2[i2])
            i2 += 1
    ans.extend(lst1[i1:])
    ans.extend(lst2[i2:])
    return ans

if __name__ == "__main__":
    print(linear_merge([1,4,5,6,9], [2,3,3,3]))

