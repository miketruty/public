""" Write a program that prints a staircase of size n.

INPUT FORMAT
  Single integer, n, denoting the size of the staircase.

OUTPUT FORMAT
  Staircase of size n, using # symbols and spaces.
  NOTE: The last line must have 0 spaces in it.

SAMPLE INPUT
  n = 4

SAMPLE OUTPUT
   #
  ##
 ###
####
"""

class InputError(Exception):
  pass


def staircase(n):
    if n < 0:
      raise InputError('Invalid input')

    if n == 0:
      print ''
    else:
      for i in xrange(n):
        print '%s%s' % (' ' * (n - i - 1), '#' * (i + 1))


def main():
  print 'Try runpytests to exercise code.'


if __name__ == '__main__':
    main()
