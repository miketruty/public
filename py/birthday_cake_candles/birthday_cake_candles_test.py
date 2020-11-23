""" Test for module: <question.py>
"""
import logging
import unittest

from birthday_cake_candles import InvalidInputError
from birthday_cake_candles import birthdayCakeCandles

# For validating print output.
from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
# _LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    common_test_data = [
      [[3, 2, 1, 3], '2\n'],
    ]

    boundary_test_data = [
      [[1], '1\n'],
      [[1000], '1\n'],
      [[1000, 1000], '2\n'],
    ]

    invalid_test_data = [
      [[], 'Must supply some lengths of >0'],
      [[-1], 'Must supply some lengths of >0'],
      [[0, 1, 2, 2, 3, 3], 'Must supply some lengths of >0'],
      [[10, 20, 30, -55, 45, 55, 66], 'Must supply some lengths of >0'],
    ]

    def test_common(self):
        for test_data, expected in self.common_test_data:
          with captured_output() as (out, _):
            birthdayCakeCandles(test_data)
          self.assertEqual(out.getvalue(), expected)

    def test_boundaries(self):
        for test_data, expected in self.boundary_test_data:
          with captured_output() as (out, _):
            birthdayCakeCandles(test_data)
          self.assertEqual(out.getvalue(), expected)

    def test_invalid(self):
        for test_data, expected in self.invalid_test_data:
          with self.assertRaises(InvalidInputError) as context:
            birthdayCakeCandles(test_data)
          self.assertTrue(expected in context.exception)


if __name__ == '__main__':
  unittest.main()
