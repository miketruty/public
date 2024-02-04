#!/usr/bin/python
from collections import Counter
import sys


def main(argv):
  if len(argv) != 2:
    raise Exception('You must supply a filename.')

  filename = argv[1]
  print 'Using file %s.' % filename

  counts = Counter()
  with open(filename, 'r') as f:
    for line in f:
      words = line.split()
      if words:
        new_counts = Counter(words)
        counts.update(new_counts)

  print counts.most_common(10)


if __name__ == '__main__':
  main(sys.argv)
