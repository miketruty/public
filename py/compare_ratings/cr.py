#!/usr/bin/python
"""Compare two lists of ratings for two different individuals.

Alice and Bob each created one problem for HackerRank. A reviewer rates the two challenges, awarding points on a scale from  to  for three categories: problem clarity, originality, and difficulty.

We define the rating for Alice's challenge to be the triplet , and the rating for Bob's
challenge to be the triplet .

Your task is to find their comparison points by comparing  with ,  with , and  with .

If , then Alice is awarded  point.
If , then Bob is awarded  point.
If , then neither person receives a point.
Comparison points is the total points a person earned.

Given  and , can you compare the two challenges and print their respective comparison points?

Input Format

The first line contains  space-separated integers, , , and , describing the respective values in triplet .
The second line contains  space-separated integers, , , and , describing the respective values in triplet .

Constraints

Output Format

Print two space-separated integers denoting the respective comparison points earned by Alice and Bob.

Sample Input

5 6 7
3 6 10
Sample Output

1 1
"""


data = [
    [1, 0, 3, 0, 4, 0,],
    [1, 1, 0, 6, 1, 3,],
]


def make_one_list(list1, list2):
    return zip(list1, list2)


def score_one_list(tuple_list):
    return map(lambda x: x[0] - x[1], tuple_list)


def score_player(fn, score_list):
    return len(filter(fn, score_list))


def main():
    alice = data[0]
    bob = data[1]
    zipped = make_one_list(alice, bob)
    scored = score_one_list(zipped)
    alice_score = score_player(lambda x: x > 0, scored)
    bob_score = score_player(lambda x: x < 0, scored)
    print alice_score, bob_score


if __name__ == '__main__':
    main()
