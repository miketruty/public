""" Count the number of candles from array of n, with the longest length.

INPUT FORMAT
  First line integer, # of entries to consider.
  Scond line, space separated list of integers (heights).

OUTPUT FORMAT
  # candles to be blown out.

SAMPLE INPUT
  4
  3 2 1 3

SAMPLE OUTPUT
  2
"""

class InvalidInputError(Exception):
  pass


def birthdayCakeCandles(candle_lengths):
  if not candle_lengths:
    raise InvalidInputError('Must supply some lengths of >0')

  if len(filter(lambda x: x <= 0, candle_lengths)) > 0:
    raise InvalidInputError('Must supply some lengths of >0')

  # Would be simple to do with collections.Counter.
  # Instead just track the max count.
  max_length = 0
  max_count = 0

  for l in candle_lengths:
    if l > max_length:
      max_length = l
      max_count = 1
    elif l == max_length:
      max_count += 1

  print max_count
  return max_count  # Sample code relies on this unlike other questions.


def main():
  print 'Try runpytests to exercise code.'


if __name__ == '__main__':
    main()
