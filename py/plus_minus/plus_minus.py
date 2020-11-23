"""
Given an array of integers, calculate the fractions of its elements that are positive, negative, and are zeros. Print the decimal value of each fraction on a new line.

Note: This challenge introduces precision problems. The test cases are scaled to six decimal places, though answers with absolute error of up to  are acceptable.

Input Format

The first line contains an integer, , denoting the size of the array.
The second line contains  space-separated integers describing an array of numbers .

Output Format

You must print the following  lines:

A decimal representing of the fraction of positive numbers in the array compared to its size.
A decimal representing of the fraction of negative numbers in the array compared to its size.
A decimal representing of the fraction of zeros in the array compared to its size.
Sample Input

6
-4 3 -9 0 4 1
Sample Output

0.500000
0.333333
0.166667
"""

import collections


def plusMinus(arr):
  if not arr:
      print '%5f' % 0.0
      print '%5f' % 0.0
      print '%5f' % 0.0
      return

  counter = collections.Counter()
  length = len(arr) * 1.0

  for value in arr:
    if not value:
      counter['zero'] += 1
    elif value < 0:
      counter['neg'] += 1
    else:
      counter['pos'] += 1

  print '%.5f' % (counter['pos'] / length)
  print '%.5f' % (counter['neg'] / length)
  print '%.5f' % (counter['zero'] / length)


def main():
  print 'Try runpytests to exercise code.'


if __name__ == '__main__':
    main()
