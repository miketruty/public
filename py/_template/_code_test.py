""" Test for module: <question.py>
"""
import logging
import unittest

from <question.py> import <InvalidXXError>
from <question.py> import <question>

# For validating print output.
# from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
# _LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    common_test_data = [
      # Can include expected print output in a tuple with data.
    ]

    boundary_test_data = [
      # Can include expected print output in a tuple with data.
    ]

    invalid_test_data = [
      # Can include expected print output in a tuple with data.
    ]

    def test_common(self):
        for test_data, expected in self.common_test_data:
          self.assertEqual(question(test_data), expected)

    def test_boundaries(self):
        for test_data, expected in self.boundary_test_data:
          self.assertEqual(question(test_data), expected)

    def test_invalid(self):
        for test_data, expected in self.invalid_test_data:
          with self.assertRaises(InvalidXXError) as context:
            question(test_data)
          self.assertTrue('ExceptionText' in context.exception)

    def test_PrintResults(self):
      with captured_output() as (out, _):
        PrintResults()


if __name__ == '__main__':
  unittest.main()
