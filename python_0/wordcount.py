"""Wordcount exercise
Google's Python class
The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.
1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...
Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.
2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.
Use str.split() (no arguments) to split on all whitespace.
Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.
Optional: define a helper function to avoid code duplication inside
print_words() and print_top().
"""

import sys


# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.

def readf(f):
    d = dict()
    f = open(f, 'r')
    w = f.read().split()
    f.close()
    for word in w:
        word = word.lower()
        if word in d.keys():
            d[word] += 1
        else:
            d[word] = 1
    return d


def print_words(f):
    d = readf(f)
    for word, cnt in sorted(d.items()):
        print(word, cnt)


def print_top(f):
    d = readf(f)
    d = sorted(zip(d.values(), d.keys()))
    n = len(d)
    for cnt, word in d[:-21:-1]:
        print(word, cnt)


def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)


if __name__ == '__main__':
    main()