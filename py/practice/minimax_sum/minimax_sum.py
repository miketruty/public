""" Find min and max calculated from summing 4 of 5 ints.

Inputs are always positive.

INPUT FORMAT
  Single line of five space-separated integers.

OUTPUT FORMAT
  2 space-separated long integers dentoting min and max values.

SAMPLE INPUT
  1 2 3 4 5

SAMPLE OUTPUT
  10 14
"""

class InvalidInputError(Exception):
  pass


def miniMaxSum(arr):
    if len(arr) != 5 or len(filter(lambda x: x < 1, arr)):
      raise InvalidInputError('Must supply 5 positive ints')

    # Do not seem to need to convert to long.
    sorted_arr = sorted(arr)
    print '%s %s' % (
      sum(sorted_arr[:4]),
      sum(sorted_arr[1:])
    )


def main():
  print 'Try runpytests to exercise code.'


if __name__ == '__main__':
    main()
