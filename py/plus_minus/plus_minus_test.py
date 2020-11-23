""" Test for module: plus_minus.py
"""
import logging
import unittest

from helper_test_contexts import captured_output
from plus_minus import plusMinus

# Use _LOGGER.debug() to debug print.
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
# _LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    common_test_data = [
        ([1, 2, 0, 4, -3, -6, 55, 0, 7],
        '0.55556\n0.22222\n0.22222\n'),
        ([1, 2, 3],
        '1.00000\n0.00000\n0.00000\n'),
        ([-33, -66, -4],
        '0.00000\n1.00000\n0.00000\n'),
        ([1, 2, 3, -2, 0],
        '0.60000\n0.20000\n0.20000\n'),
        ([-33, -66, -4, 0, 0],
        '0.00000\n0.60000\n0.40000\n'),
    ]

    boundary_test_data = [
        ([1],
        '1.00000\n0.00000\n0.00000\n'),
        ([0],
        '0.00000\n0.00000\n1.00000\n'),
        ([-1],
        '0.00000\n1.00000\n0.00000\n'),
    ]

    invalid_test_data = [
        ([], ''),
    ]

    def test_common(self):
        for test_data, expected in self.common_test_data:
            with captured_output() as (out, _):
                plusMinus(test_data)

            self.assertEqual(out.getvalue(), expected)

    def test_boundaries(self):
        for test_data, expected in self.boundary_test_data:
            with captured_output() as (out, _):
                plusMinus(test_data)

            self.assertEqual(out.getvalue(), expected)

    def test_invalid(self):
        for test_data, expected in self.boundary_test_data:
            with captured_output() as (out, _):
                plusMinus(test_data)

            self.assertEqual(out.getvalue(), expected)


if __name__ == '__main__':
  unittest.main()
