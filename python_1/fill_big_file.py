
with open('big_file.txt', mode='w') as f:
    for i in range(int(1e8)):
        print('curious', end='', file=f)