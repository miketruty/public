""" Test for module: staircase.py
"""
import logging
import unittest

from staircase import InputError
from staircase import staircase

# For validating print output.
from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
# _LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    common_test_data = [
      # Can include expected print output in a tuple with data.
      [1, '#\n'],
      [2, ' #\n##\n'],
      [3, '  #\n ##\n###\n'],
      [4, '   #\n  ##\n ###\n####\n'],
      [5, '    #\n   ##\n  ###\n ####\n#####\n'],
    ]

    boundary_test_data = [
      # Can include expected print output in a tuple with data.
      [0, '\n'],
    ]

    invalid_test_data = [
      # Can include expected print output in a tuple with data.
      [-1, 'Invalid input'],
    ]

    def test_common(self):
        for test_data, expected in self.common_test_data:
          with captured_output() as (out, _):
            staircase(test_data)
          self.assertEqual(out.getvalue(), expected)

    def test_boundaries(self):
        for test_data, expected in self.boundary_test_data:
          with captured_output() as (out, _):
            staircase(test_data)
          self.assertEqual(out.getvalue(), expected)

    def test_invalid(self):
        for test_data, expected in self.invalid_test_data:
          with self.assertRaises(InputError) as context:
            staircase(test_data)
          self.assertTrue('Invalid input' in context.exception)


if __name__ == '__main__':
  unittest.main()
