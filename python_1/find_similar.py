import sys
import os
from hashlib import sha1
from collections import defaultdict
import re

BLOCK = 36101


def get_hash(file_path):
    with open(file_path, mode='rb') as f:
        hasher = sha1()
        block = f.read(BLOCK)
        while block:
            hasher.update(block)
            block = f.read(BLOCK)
        return hasher.hexdigest()


def collect_files(to_find, wrong):
    hashes = defaultdict(list)
    for path, _, files in os.walk(to_find):
        for file in files:
            if not wrong.match(file):
                file_path = os.path.join(path, file)
                hashes[get_hash(file_path)].append(os.path.abspath(file_path))
    return hashes


def main():
    if len(sys.argv) != 2:
        print('usage: find_similar.py dir')
        sys.exit(1)
    to_find = sys.argv[1]
    wrong = re.compile('[.~].*')
    hashes = collect_files(to_find, wrong)
    for files in hashes.values():
        if len(files) > 1:
            print(*files, sep=':')


if __name__ == '__main__':
    main()