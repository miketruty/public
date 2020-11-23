""" Test for module: <question.py>
"""
import logging
import unittest

from is_anagram import InvalidInputError
from is_anagram import is_anagram

# For validating print output.
# from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
# _LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    common_test_data = [
      # Can include expected print output in a tuple with data.
      [['abc', 'cba'], True],
      [['abc', 'ba'], False],
      [['abc', 'ca'], False],
      [['abc', 'cb'], False],
      [['abcdefg', 'badcfeg'], True],
    ]

    boundary_test_data = [
      # Can include expected print output in a tuple with data.
      [['a', 'b'], False],
      [['b', 'a'], False],
      [['a', 'a'], True],
      [['z', 'z'], True],
      [['z', 'zz'], False],
      [['zz', 'z'], False],
    ]

    invalid_test_data = [
      # Can include expected print output in a tuple with data.
      [[None, 'a'], 'Two non-empty strings must be supplied.'],
      [['a', None], 'Two non-empty strings must be supplied.'],
      [['', 'a'], 'Two non-empty strings must be supplied.'],
      [['a', ''], 'Two non-empty strings must be supplied.'],
    ]

    def test_common(self):
        for (s1, s2), expected in self.common_test_data:
          self.assertEqual(is_anagram(s1, s2), expected)

    def test_boundaries(self):
        for (s1, s2), expected in self.boundary_test_data:
          self.assertEqual(is_anagram(s1, s2), expected)

    def test_invalid(self):
        for (s1, s2), expected in self.invalid_test_data:
          with self.assertRaises(InvalidInputError) as context:
            is_anagram(s1, s2)
          self.assertTrue(expected in context.exception)


if __name__ == '__main__':
  unittest.main()
