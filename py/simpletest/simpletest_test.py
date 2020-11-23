""" Test for module: <question.py>
"""
import logging
import unittest

from simpletest import ReturnOne, ReturnTwo
from simpletest import PrintResults

# For validating print output.
from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
# _LOGGER = logging.getLogger(__name__)
# _LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
# _LOGGER.setLevel(logging.DEBUG)


class TestQuestion(unittest.TestCase):

    def test_ReturnOne(self):
      self.assertEqual(ReturnOne(), 1)

    def test_ReturnTwo(self):
      self.assertEqual(ReturnTwo(), 2)

    def test_PrintResults(self):
      with captured_output() as (out, _):
        PrintResults()



if __name__ == '__main__':
  unittest.main()
