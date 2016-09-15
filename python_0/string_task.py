#!/usr/bin/env python


def verbing(s):
    if len(s) > 2 and s[-3:] == 'ing':
        return s + 'ly'
    elif len(s) > 2:
        return s + 'ing'
    else:
        return s
    return


def not_bad(s):
    start = s.find('not')
    end = s.find('bad') + 3
    if end > start and end != -2 and start != -1:
        return s[:start] + 'good' + s[end:]
    return s


def front_back(a, b):
    la = (len(a) + 1) // 2
    lb = (len(b) + 1) // 2
    return a[:la] + b[:lb] + a[la:] + b[lb:]


if __name__ == "__main__":
    print(verbing('sa'), verbing('saa'), verbing('sing'))
    print(not_bad('sanotbad'), not_bad('saanotyybad'), not_bad('sibadngnotfghj'), not_bad('snotibadngnotfghjbad'), not_bad('jnotkjklj'))
    print(not_bad('notsanotbad'), not_bad('saanotyybad'), not_bad('notsibadngnotfghj'), not_bad('snotibadngnotfghjbad'), not_bad('jnotkjklj'))
#   print(front_back('abcd', 'xy'), front_back('saa', ''), front_back('singe', 'afo'))
