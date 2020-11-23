""" simpletest demonstrates very simple use of unit tests.

INPUT FORMAT
  None

OUTPUT FORMAT
  One line of text.

SAMPLE INPUT
  None

SAMPLE OUTPUT
  One: 1. Two: 2.
"""

# ReturnOne is a public function that returns 1.
def ReturnOne():
  return 1


# ReturnTwo is a private function that returns 2.
def ReturnTwo():
  return 2


def PrintResults():
  print 'One: %d. Two: %d.' % (ReturnOne(), ReturnTwo())


def main():
  PrintResults()


if __name__ == '__main__':
    main()
