#!/usr/bin/python
"""Compare 2 csv files of video ids."""

import argparse
import csv
import os
import sys


def _ParseFlags(argv):
  parser = argparse.ArgumentParser(description='Compare 2 CSV files.')
  parser.add_argument(
      '--csv1',
      type=str,
      required=True,
      help='Required /fullpath/filename1.csv.')
  parser.add_argument(
      '--csv2',
      type=str,
      required=True,
      help='Required /fullpath/filename2.csv.')
  flags = parser.parse_args(argv)

  if not os.path.isfile(flags.csv1):
    print 'Error: cannot find csv1 file: %s.' % flags.csv1
    sys.exit(-1)
  if not os.path.isfile(flags.csv2):
    print 'Error: cannot find csv2 file: %s.' % flags.csv2
    sys.exit(-1)

  return flags


def _CompareCSVs(csv1, csv2):
  video_ids_one_set = set()
  video_ids_two_set = set()

  with open(csv1, 'r') as f1:
    for r in csv.reader(f1):
      video_ids_one_set.add(r[0])

  with open(csv2, 'r') as f2:
    for r in csv.reader(f2):
      video_ids_two_set.add(r[0])

  print 'Found %s ids in %s.' % (len(video_ids_one_set), csv1)
  print 'Found %s ids in %s.' % (len(video_ids_two_set), csv2)

  print 'Diff: %s.' % str(video_ids_one_set - video_ids_two_set)


def main(argv):
  flags = _ParseFlags(argv)
  _CompareCSVs(flags.csv1, flags.csv2)


if __name__ == '__main__':
  main(sys.argv[1:])
