#!/usr/bin/python
"""Generate metadata files from curated metadata csv.

   Usually a file named: data/curated_video_data.csv exported from Sheets.
"""

import argparse
import csv
import json
import os
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
FIELD_TAGS = 'tags'  # New from original curated csv.
FIELD_IMAGE = 'image'  # New from original curated csv.

REST_KEY = 'rest_key'  # Used to capture extra fields

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
    FIELD_TAGS,
    FIELD_IMAGE,
    FIELD_VIDEO_ID,
    FIELD_SESSION_ID,
]

METADATA_DEFAULT = {
    FIELD_UNIQUE_ID: '',
    FIELD_TITLE: '',
    FIELD_EVENT: '',
    FIELD_VIEW_COUNT: 0,
    FIELD_SUBTITLE: '',
    FIELD_DURATION: 0,
    FIELD_SPEAKERS: '',
    FIELD_DESC: '',
    FIELD_PUB_DATE: '',
    FIELD_SLIDES_LINK: '',
    FIELD_TAGS: '',
    FIELD_IMAGE: '',
    FIELD_VIDEO_ID: '',
    FIELD_SESSION_ID: '',
}

FILE_TYPE_ACC = 'acc'  # accelerate videos.
FILE_TYPE_ARCH = 'arch'  # architecture articles.
FILE_TYPE_VIDEO = 'video'  # youtube videos.
FILE_TYPES_ALL = [FILE_TYPE_ACC, FILE_TYPE_ARCH, FILE_TYPE_VIDEO]


def _ParseFlags(argv):
  parser = argparse.ArgumentParser(
      description='Update csv metadata by assembling updated json files.')
  parser.add_argument(
      '-o',
      '--old_csv_file',
      type=str,
      required=True,
      help='Required /fullpath/filename.csv. The baseline metadata.')
  parser.add_argument(
      '-j',
      '--json_file_dir',
      type=str,
      required=True,
      help='Required /fullpath/jsondir/ to find metadata updates.')
  flags = parser.parse_args(argv)

  if not os.path.isfile(flags.old_csv_file):
    print 'Error: cannot find old csv file: %s.' % flags.old_csv_file
    sys.exit(-1)
  if not os.path.isdir(flags.json_file_dir):
    print 'Error: cannot find json file dir: %s.' % flags.json_file_dir
    sys.exit(-1)

  return flags


def _EncodeIfNeeded(s):
  # Helper to handle unicode when needed
  if isinstance(s, unicode):
    return s.encode('utf-8')
  return s


def _CreateCSVFileFromDicts(row_dicts):
  # write the new csv file
  new_csv_file = tempfile.mkstemp(suffix='.csv', prefix='new_meta')[1]
  with open(new_csv_file, 'wb') as f:
    writer = csv.DictWriter(f, FIELDS, lineterminator='\n')
    # We don't write a header.
    for D in row_dicts:
      try:
        writer.writerow(
            {k: _EncodeIfNeeded(v) for k,v in D.items()})
      except UnicodeEncodeError as e:
        print 'UnicodeEncodeError: %s\n%s' % (e, D)
        raise
      except UnicodeDecodeError as e:
        print 'UnicodeDecodeError: %s\n%s' % (e, D)
        raise
      except ValueError as e:
        print 40 * '-'
        import pprint
        pprint.pprint(D)
        raise

  print 'Created %s file with %s rows.' % (new_csv_file, len(row_dicts))


def _CreateFileFromDict(json_file_path, row_dict):
  with open(json_file_path, 'w') as jf:
    json.dump(row_dict, jf, indent=2, separators=(',', ': '), sort_keys=True)


def _LoadJsonFromFile(json_file_path):
  with open(json_file_path, 'r') as jf:
    # Using ASCII. If error (e.g. left-single-quote), fix in the JSON files.
    print 'Parsing %s.' % json_file_path
    try:
      file_dict = json.load(jf, 'utf-8')
    except UnicodeDecodeError as e:
      # Cannot handle international characters.
      # TODO(truty): fix support for unicode - mostly to allow for speakers
      #       names with special characters.
      msg = ('Unable to decode characters in %s. Please fix  (%s).' %
             (json_file_path, e))
      print msg
      sys.exit(-1)
  # Fix old data files that do not have 'unique_id' and 'session_id'.
  if (FIELD_UNIQUE_ID not in file_dict) or (FIELD_SESSION_ID not in file_dict):
    # Update the dict and write the file.
    if FIELD_UNIQUE_ID not in file_dict:
      # 'video_id' MUST be present. Copy from it.
      file_dict[FIELD_UNIQUE_ID] = file_dict[FIELD_VIDEO_ID]
    if FIELD_SESSION_ID not in file_dict:
      # Only added at next2018.
      file_dict[FIELD_SESSION_ID] = ''
    _CreateFileFromDict(json_file_path, file_dict)
  return file_dict


def _UpdateMetadataFromDict(metadata, unique_id, file_dict, file_path):
  change_count = 0
  new_unique_id = file_dict.get(FIELD_UNIQUE_ID, file_dict.get(
      FIELD_SESSION_ID, file_dict.get(FIELD_VIDEO_ID)))
  if not new_unique_id:
    print 'Unable to find unique ID.'
    import pprint
    pprint.pprint(file_dict)
    sys.exit(-1)

  # New field tags.
  # metadata[unique_id][FIELD_TAGS] = ''

  for k in sorted(file_dict.keys()):
    # We ignore speaker1 and speaker2 when creating the csv.
    if k in [FIELD_SPEAKER1_EMAIL, FIELD_SPEAKER2_EMAIL]:
      if k in metadata[unique_id]:
        del metadata[unique_id][k]
      continue

    # view_count populated outside of this (authors don't set view_count).
    if k == FIELD_VIEW_COUNT:
      continue

    # We're going to save to csv so let's just get it to str now.
    try:
      s = unicode(file_dict[k]).encode('utf-8')
    except UnicodeEncodeError as e:
      # We use csv for read/write and it doesn't support reading/writing
      # Unicode.
      msg = ('File %s has characters outside range(128). Please fix (%s).' %
             (file_path, e))
      print msg
      return -1  # Indicate a problem.

    current_metadata = metadata[unique_id].get(k)
    if current_metadata != s:
      change_count += 1
      metadata[unique_id][k] = file_dict[k]

  if unique_id != new_unique_id:
    print '*' * 40
    print 'Unique ID updated (%s => %s)!' % (unique_id, new_unique_id)

    metadata[new_unique_id] = metadata[unique_id]
    del metadata[unique_id]
    print metadata[new_unique_id]
  return change_count


def _ParseMetaFileName(json_file):
  for t in FILE_TYPES_ALL:
    if json_file.startswith(t):
      return t, (json_file.split('.')[0][len(t):])
  print 'Error: unexpected json file: %s.' % json_file
  sys.exit(-1)


def _AssembleFilesIntoCSVMetadata(old_csv_file, json_file_dir):
  # read the old csv file into a dictionary.
  # A lot of this is tracking to print sensible accounting messages.
  metadata = {}
  metadata_entries_count = 0
  metadata_files_count = 0
  metadata_files_changed_count = 0
  change_count = 0
  metadata_files_added_set = set()

  # Baseline on the old/original csv file.
  print 'Reading %s.' % old_csv_file
  with open(old_csv_file, 'rb') as cf:
    reader = csv.DictReader(cf, fieldnames=FIELDS, restkey=REST_KEY)
    for row_dict in reader:
      if REST_KEY in row_dict:
        del row_dict[REST_KEY]
      metadata_entries_count += 1
      metadata[row_dict.get(FIELD_UNIQUE_ID)] = row_dict
  print 'Read %s entries from %s.' % (metadata_entries_count, old_csv_file)

  # Look through json files for updates.
  conversion_problems_found = False
  for root, unused_dirs, json_files in os.walk(json_file_dir):
    for json_file in json_files:
      if json_file in ['video_template.json', 'solution_template.json']:
        continue
      metadata_files_count += 1

      json_file_path = os.path.join(root, json_file)
      file_dict = _LoadJsonFromFile(json_file_path)

      # Ugly, depends on tribal knowledge that the file is named
      # video<unique_id>.json or arch<unique_id.json
      json_file_type, unique_id = _ParseMetaFileName(json_file)

      if unique_id not in metadata:
        metadata_files_added_set.add(unique_id)

        new_metadata = METADATA_DEFAULT.copy()
        new_metadata[FIELD_UNIQUE_ID] = unique_id
        metadata[unique_id] = new_metadata

      change_count_delta = _UpdateMetadataFromDict(metadata, unique_id,
                                                   file_dict, json_file_path)
      if change_count_delta == -1:
        conversion_problems_found = True
        continue
      if change_count_delta:
        change_count += change_count_delta
        metadata_files_changed_count += 1

  if conversion_problems_found:
    print 'Exiting without creating file.'
    sys.exit(-1)

  print 'Found %s metadata files.' % metadata_files_count
  print 'Added %s new metadata files %s.' % (
      len(metadata_files_added_set), sorted(metadata_files_added_set))
  print 'Found %s metadata files with changes.' % metadata_files_changed_count
  print 'Found %s metadata fields changed.' % change_count

  try:
    row_dicts = sorted(metadata.values(),
                       key=lambda x: _EncodeIfNeeded(x[FIELD_TITLE]))
  except UnicodeDecodeError as e:
    print 'UnicodeDecodeError: %s' % e
    raise
  _CreateCSVFileFromDicts(row_dicts)


def main(argv):
  flags = _ParseFlags(argv)
  _AssembleFilesIntoCSVMetadata(flags.old_csv_file, flags.json_file_dir)


if __name__ == '__main__':
  main(sys.argv[1:])
