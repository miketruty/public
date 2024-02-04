""" Test for module: <question.py>
"""
import logging
import unittest

from minimax_sum import InvalidInputError
from minimax_sum import miniMaxSum

# For validating print output.
from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
_LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    common_test_data = [
      [[1, 2, 3, 4, 5], '10 14\n'],
      [[1, 20, 3, 44, 15], '39 82\n'],
    ]

    boundary_test_data = [
      # 0xFFFFFFFF is largest possible 32bit int.
      [[0xFFFFFFFA, 0xFFFFFFFF, 0xFFFFFFFE,
        0xFFFFFFFB, 0xFFFFFFFC],
        '17179869167 17179869172\n'],
    ]

    invalid_test_data = [
      [[0, 1, 2, 3, 4], 'Must supply 5 positive ints'],
      [[1], 'Must supply 5 positive ints'],
      [[1, 2], 'Must supply 5 positive ints'],
      [[1, 2, 3], 'Must supply 5 positive ints'],
      [[1, 2, 3, 4], 'Must supply 5 positive ints'],
      [[1, 2, 3, 4, 5, 6], 'Must supply 5 positive ints'],
    ]

    def test_common(self):
        for test_data, expected in self.common_test_data:
          with captured_output() as (out, _):
            miniMaxSum(test_data)
          self.assertEqual(out.getvalue(), expected)

    def test_boundaries(self):
        for test_data, expected in self.boundary_test_data:
          with captured_output() as (out, _):
            miniMaxSum(test_data)
          self.assertEqual(out.getvalue(), expected)

    def test_invalid(self):
        for test_data, expected in self.invalid_test_data:
          with self.assertRaises(InvalidInputError) as context:
            miniMaxSum(test_data)
          self.assertTrue(expected in context.exception)


if __name__ == '__main__':
  unittest.main()
