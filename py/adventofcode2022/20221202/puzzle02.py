#!/usr/bin/python3
# Read the input, roshambo via shema and tally scores.

import os
import sys


def score_round_part1(round: str) -> int:
    """Score player1 vs me.

    Player1: A=rock, B=paper, C=scissors
    Player2: X=rock, Y=paper, Z=scissors

    My plays are scored:
    1=rock, 2=paper, 3=scissors
    0=loss, 3=tie, 6=win
    """
    score_answers = {
      'A X': 1+3,  # tie
      'A Y': 2+6,  # win
      'A Z': 3+0,  # loss
      'B X': 1+0,  # loss
      'B Y': 2+3,  # tie
      'B Z': 3+6,  # win
      'C X': 1+6,  # win
      'C Y': 2+0,  # loss
      'C Z': 3+3,  # tie
    }
    return score_answers.get(round, 0)


def part1_score(input_filename: str) -> int:
    """Score the given rock, paper, scissors outcome.
    a, b, c is player1 rock, paper, scissors
    x, y, zz is player2 rock, paper, scissors.
    """
    score = 0
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            score += score_round_part1(line.strip())

    return score


def score_round_part2(round: str) -> int:
    """Score player1 vs me.

    Player1: A=rock, B=paper, C=scissors
    Player2: X=lost, Y=tie, Z=win

    My plays are scored:
    1=rock, 2=paper, 3=scissors
    0=loss, 3=tie, 6=win
    """
    score_answers = {
      'A X': 3+0,  # lose, scissors
      'A Y': 1+3,  # tie, rock
      'A Z': 2+6,  # win, paper
      'B X': 1+0,  # lose, rock
      'B Y': 2+3,  # tie, paper
      'B Z': 3+6,  # win, scissors
      'C X': 2+0,  # lose, paper
      'C Y': 3+3,  # tie, scissors
      'C Z': 1+6,  # win, rock
    }
    return score_answers.get(round, 0)


def part2_score(input_filename: str) -> int:
    """Score the given rock, paper, scissors outcome.
    a, b, c is player1 rock, paper, scissors
    x, y, zz is player2 rock, paper, scissors.
    """
    score = 0
    with open(input_filename, 'rt') as input_file:
        for line in input_file:
            score += score_round_part2(line.strip())

    return score


def main(argv):
    input_filename = argv[1] if len(argv) > 1 else 'input'
    if not os.path.isfile(input_filename):
        print(f'Error: cannot find file {input_filename}')
        sys.exit(-1)
    print(part1_score(input_filename))
    print(part2_score(input_filename))


if __name__ == '__main__':
    main(sys.argv)
