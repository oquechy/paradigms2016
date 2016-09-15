import sys
import os
from hashlib import sha1
import re

BLOCK = 36101

hashes = dict()
for path, dirs, files in os.walk(sys.argv[1]):
    wrong = re.compile('[.~].*')
    for file in files:
        if not wrong.match(file):
            file_path = os.path.join(path,file)
            with open(file_path, mode='rb') as f:
                hasher = sha1()
                block = f.read(BLOCK)
                while block:
                    hasher.update(block)
                    block = f.read(BLOCK)
                hash = hasher.hexdigest()
                if hash in hashes:
                    hashes[hash].append(os.path.abspath(file_path))
                else:
                    hashes[hash] = [os.path.abspath(file_path)]


for hash, files in hashes.items():
    if len(files) > 1:
        print(*files, sep=':')
