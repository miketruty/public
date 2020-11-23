""" Determine if a string is an anagram of another.

An interesting requirement is how to handle letter case.
A simple assumption might be to ignore letter case.

INPUT FORMAT
  2 strings.

OUTPUT FORMAT
  Boolean: True or False

SAMPLE INPUT
  abcd, cbca

SAMPLE OUTPUT
  True
"""
import collections


class InvalidInputError(Exception):
    pass


def count_characters(ss):
    """Return a counter with character counts."""
    counts = collections.Counter()
    for c in ss:
        counts[c] += 1
    return counts


def is_anagram(s1, s2):
    # Could make this more efficient by walking each string manually.
    # Cannot use a set because then we lose repeated characters.
    # Lower case all to be case insensitive.
    if not s1 or not s2:
        raise InvalidInputError('Two non-empty strings must be supplied.')
    return count_characters(s1.lower()) == count_characters(s2.lower())


def main():
  print 'Try runpytests to exercise code.'


if __name__ == '__main__':
    main()