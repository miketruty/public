#!/usr/bin/python
"""Generate metadata files from curated metadata csv."""

import argparse
import csv
import json
import os
import shutil
import sys
import tempfile

# Matches config.py FIELDs
FIELD_DESC = 'description'
FIELD_DURATION = 'duration_min'
FIELD_EMPTYSTRING1 = 'estring1'
FIELD_PUB_DATE = 'published_date'
FIELD_TITLE = 'title'
FIELD_UNIQUE_ID = 'unique_id'
FIELD_VIEW_COUNT = 'views'
FIELD_VIDEO_ID = 'video_id'
FIELD_SESSION_ID = 'session_id'

# Custom from script or hand-curated metadata (sheet).
FIELD_EVENT = 'event'
FIELD_SLIDES_LINK = 'slides_link'
FIELD_SPEAKERS = 'speakers'
FIELD_SPEAKER1_EMAIL = 'speaker1'
FIELD_SPEAKER2_EMAIL = 'speaker2'
FIELD_SUBTITLE = 'subtitle'
FIELD_TAGS = 'tags'  # Not in original curated metadata.
FIELD_IMAGE = 'image'  # For non-videos.

FIELDS = [
    FIELD_UNIQUE_ID,
    FIELD_TITLE,
    FIELD_EVENT,
    FIELD_VIEW_COUNT,
    FIELD_SUBTITLE,
    FIELD_DURATION,
    FIELD_SPEAKERS,
    FIELD_DESC,
    FIELD_PUB_DATE,
    FIELD_SLIDES_LINK,
    FIELD_SPEAKER1_EMAIL,
    FIELD_SPEAKER2_EMAIL,
    FIELD_TAGS,
    FIELD_IMAGE,
    FIELD_VIDEO_ID,
    FIELD_SESSION_ID,
]

FILE_TYPE_ACC = 'acc'  # accelerate videos.
FILE_TYPE_ARCH = 'arch'  # architecture articles.
FILE_TYPE_VIDEO = 'video'  # youtube videos.
FILE_TYPES_ALL = [FILE_TYPE_ACC, FILE_TYPE_ARCH, FILE_TYPE_VIDEO]


def _ParseFlags(argv):
  parser = argparse.ArgumentParser(
      description='Parse YouTube metadata into reviewable chunks (files).')
  parser.add_argument(
      '-c',
      '--csv_file',
      type=str,
      required=True,
      help='Required /fullpath/filename.csv.')
  parser.add_argument(
      '-t',
      '--csv_file_type',
      type=str,
      required=True,
      help='Required: either "video" or "arch" (for architectures).')
  flags = parser.parse_args(argv)

  if flags.csv_file_type not in FILE_TYPES_ALL:
    print 'Error: csv_file_type must be in %s.' % FILE_TYPES_ALL
    sys.exit(-1)
  return flags


def _CreateFileFromDict(json_file, row_dict):
  with open(json_file, 'w') as jf:
    json.dump(row_dict, jf, indent=2, separators=(',', ': '), sort_keys=True)


def _StripHeader(csv_file):
  # This should be written to read/write lines in chunks, not this way.
  # But our files aren't that large right now (<1000 lines).
  new_csv_file = tempfile.mkstemp(suffix='.csv', prefix='strip_meta')[1]
  with open(csv_file, 'rb') as input_f:
    first_line = input_f.readline()
    if not first_line.startswith('Unique ID'):
      shutil.copyfile(csv_file, new_csv_file)
    else:
      with open(new_csv_file, 'wb') as output_f:
        # The earlier readline absorbed the first line.
        output_f.writelines(input_f.readlines())

  return new_csv_file


def _CreateFilesFromCSVMetadata(csv_file, csv_file_type):
  if not os.path.isfile(csv_file):
    print 'Cannot find file %s.' % csv_file
    sys.exit(-1)

  cl_data = {}
  i = 0
  temp_file_dir = tempfile.mkdtemp(prefix='reviewdeo')
  with open(csv_file, 'r') as cf:
    # Expect NO header and proper field order in the csv.
    reader = csv.DictReader(cf, fieldnames=FIELDS)
    for row_dict in reader:
      i += 1
      json_file = os.path.join(temp_file_dir, '%s%s.json' %
                               (csv_file_type, row_dict[FIELD_UNIQUE_ID]))

      unique_id = row_dict[FIELD_UNIQUE_ID]
      title = row_dict[FIELD_TITLE]
      event = row_dict[FIELD_EVENT]
      if (not unique_id) or (not title) or (not event):
        print('MISSING field from line %s. '
              '[unique_id=%s, title=%s, event=%s]' %
              (i, unique_id, title, event))
        print 'Skipping file %s.' % json_file
        continue

      _CreateFileFromDict(json_file, row_dict)
      cl_data[row_dict[FIELD_UNIQUE_ID]] = {
          FIELD_TITLE: row_dict[FIELD_TITLE],
          FIELD_EVENT: row_dict[FIELD_EVENT],
          FIELD_SPEAKER1_EMAIL: row_dict.get(FIELD_SPEAKER1_EMAIL, ''),
          FIELD_SPEAKER2_EMAIL: row_dict.get(FIELD_SPEAKER2_EMAIL, ''),
      }
  if cl_data:
    json_file = os.path.join(temp_file_dir, 'cl_data.json')
    _CreateFileFromDict(json_file, cl_data)
  print 'Created %s files from %s (%s lines) in %s.' % (len(cl_data), csv_file,
                                                        i, temp_file_dir)


def main(argv):
  flags = _ParseFlags(argv)
  _CreateFilesFromCSVMetadata(
      _StripHeader(flags.csv_file), flags.csv_file_type)


if __name__ == '__main__':
  main(sys.argv[1:])
