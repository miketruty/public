""" Test for module: flashcard.py
"""
import logging
import random
import unittest

from flashcard import do_exam

from flashcard import InvalidDataError

# For validating print output.
from helper_test_contexts import captured_output

# Use _LOGGER.debug() to debug print to file.
_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.FileHandler('testlog.debuglog'))
_LOGGER.setLevel(logging.DEBUG)


class TestFlashcards(unittest.TestCase):

    good_file_tests = [
        [['./data/computers.json'],
         ['17 ns', '200'],
         '1) Mutex lock/unlock time (ns)?\n\n==>Correct!\n'
         'You\'re 1 for 1; that\'s 100%.\n'
         '2) Read sequentially from HDD at a rate of x MB per second?\n\n==>Correct!\n'
         'Your score was: 2/2. Exiting now.'],
        [['./data/entertainment.json'],
         ['50b', '35b'],
         '1) Theater box office annual revenue (b)?\n\n==>Correct!\n'
         'You\'re 1 for 1; that\'s 100%.\n'
         '2) EMEA Gaming entertainment annual revenue (b)?\n\n==>Correct!\n'
         'Your score was: 2/2. Exiting now.'],
        [['./data/population.json'],
         ['4.6b', '115m'],
         '1) Population of continent: Europe (#3)?\n\n==>Correct!\n'
         'You\'re 1 for 1; that\'s 100%.\n'
         '2) Population of Ethiopia (#12)?\n\n==>Correct!\n'
         'Your score was: 2/2. Exiting now.'],
        [['./data/sports_market.json'],
         ['200m', '9'],
         '1) CFL annual revenue (#6)?\n\n==>Correct!\n'
         'You\'re 1 for 1; that\'s 100%.\n'
         '2) #CFL teams?\n\n==>Correct!\n'
         'Your score was: 2/2. Exiting now.'],
    ]

    bad_file_tests = [
        [['./data/sports_market_err1.json'],
          'ERROR: mis-formed data!'],
        [['./data/sports_market_err2.json'],
          'ERROR: mis-formed exam, question 1.'],
        [['./data/sports_market_err3.json'],
          'ERROR: mis-formed exam, question 2.'],
        [['./data/sports_market_err_badjson.json'],
          'ERROR: mis-formed JSON in ./data/sports_market_err_badjson.json!'],
    ]

    def test_good_data(self):
        for test_data, inputs, expected in self.good_file_tests:
            with captured_output() as (out, _):
                _LOGGER.debug('Check {} for {}.'.format(test_data, expected))
                random.seed(1) # Ensure questions asked in same order
                do_exam(test_data, inputs, len(inputs))
            self.assertEqual(out.getvalue().strip(), expected,
                             '\n' + out.getvalue().strip() + ' !=\n' + expected)

    def test_json_errors(self):
        for test_data, expected in self.bad_file_tests:
            with self.assertRaises(InvalidDataError) as context:
                _LOGGER.debug('Check {} for {}.'.format(test_data, expected))
                do_exam(test_data)
            self.assertTrue(expected in context.exception, context.exception)


if __name__ == '__main__':
  unittest.main()

