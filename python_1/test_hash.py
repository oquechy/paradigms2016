from hashlib import sha1
import time

times = dict()

for BLOCK in range(1, 70000, 100):
    with open('big_file_2.txt', mode='rb') as inp:
        hasher = sha1()
        block = inp.read(BLOCK)
        start = time.time()
        while block:
            hasher.update(block)
            block = inp.read(BLOCK)
        times[time.time() - start] = BLOCK

print(min(times.items()), file=open('hash_test_result.txt', 'w'))