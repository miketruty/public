#!/usr/bin/python
"""Using YouTube data api retrieve video metadata.

Requires apicliient from Google Cloud Client Libraries.
"""

import argparse
import csv
import re
import sys
import tempfile

from apiclient.discovery import build

# Matches config.py FIELDs
FIELD_DESC = 'description'
FIELD_DURATION = 'duration_min'
FIELD_EMPTYSTRING1 = 'estring1'
FIELD_PUB_DATE = 'published_date'
FIELD_TITLE = 'title'
FIELD_VIDEO_ID = 'video_id'
FIELD_VIEW_COUNT = 'views'

# Custom from script or hand-curated metadata (sheet).
FIELD_EVENT = 'event'
FIELD_SPEAKERS = 'speakers'
FIELD_SUBTITLE = 'subtitle'

FIELDS = [
    FIELD_VIDEO_ID,
    FIELD_TITLE,
    FIELD_EVENT,
    FIELD_VIEW_COUNT,
    FIELD_SUBTITLE,
    FIELD_DURATION,
    FIELD_SPEAKERS,
    FIELD_DESC,
    FIELD_PUB_DATE,
]

_DURATION_HOURS_REGEX = re.compile(r'(\d+)H')
_DURATION_MINUTES_REGEX = re.compile(r'(\d+)M')
_DURATION_SECONDS_REGEX = re.compile(r'(\d+)S')

_ENCODING = 'utf-8'

_OLD_EVENTS = [
    ['next2016', 'PLsmceK7t6HVpjXQ8Ol3N26fbt3xBHOPxn'],
    ['next2017', 'PLIivdWyY5sqI8RuUibiH8sMb1ExIw0lAR'],
    ['next2018', 'PLBgogxgQVM9v0xG0QTFQ5PTbNrj8uGSS-'],
    ['next2019', 'PLIivdWyY5sqIXvUGVrFuZibCUdKVzEoUw'],
]

_EVENTS = [
    ['next2020', 'PLIivdWyY5sqLwPxvq9Fy0dl3Y_pbRg1_L'],
]

_MAX_RESULTS = 50  # Max possible is 50, default is 5.

_YOUTUBE_API_SERVICE_NAME = 'youtube'
_YOUTUBE_API_VERSION = 'v3'


def _ConvertPTToMinutes(pt_string):
  # durations = ['PT2H14M41S', 'PT17M33S', 'PT3M59S', 'PT2H19M5S']
  hours = 0
  minutes = 0
  seconds = 0
  m = _DURATION_HOURS_REGEX.search(pt_string)
  if m:
    hours = int(m.groups()[0])
  m = _DURATION_MINUTES_REGEX.search(pt_string)
  if m:
    minutes = int(m.groups()[0])
  m = _DURATION_SECONDS_REGEX.search(pt_string)
  if m:
    seconds = int(m.groups()[0])
  return int((hours * 60) + minutes + round(float(seconds) / float(60)))


def _Encode(string_field):
  return string_field.encode(_ENCODING)


def _ParseFlags(argv):
  parser = argparse.ArgumentParser(
      description='Grab YouTube data from a playlist.')
  parser.add_argument(
      '-k',
      '--dev_key',
      type=str,
      required=True,
      help='Required DEVELOPER_KEY for API key.')
  flags = parser.parse_args(argv)
  return flags


def _BuildYouTubeService(dev_key):
  return build(
      _YOUTUBE_API_SERVICE_NAME, _YOUTUBE_API_VERSION, developerKey=dev_key)


class YTPlaylistService(object):

  def __init__(self, dev_key):
    self._youtube = _BuildYouTubeService(dev_key)

  def _MakeListRequest(self, playlist_id, max_results):
    print('Videos in list %s' % playlist_id)
    return self._youtube.playlistItems().list(
        playlistId=playlist_id, part='snippet', maxResults=max_results)

  def _NextListRequest(self, request, response):
    return self._youtube.playlistItems().list_next(request, response)

  def _ListVideoDurations(self, video_ids):
    durations = {}
    # Get the durations for the last set of video ids.
    # More efficient than calling this separately for each.
    video_response = self._youtube.videos().list(
        id=','.join(video_ids), part='contentDetails').execute()
    for item in video_response['items']:
      durations[item['id']] = _ConvertPTToMinutes(
          item['contentDetails']['duration'])
    return durations

  def GetPlaylistMetadata(self, playlist_id, event_tag):
    results = []  # List of dictionaries.
    request = self._MakeListRequest(playlist_id, _MAX_RESULTS)

    # Get video_id, title, description, everything except duration.
    while request:
      videos = []
      video_ids = []
      response = request.execute()

      for playlist_item in response['items']:
        video = {}
        # Thumbnails are here too if we need them.
        video[FIELD_TITLE] = _Encode(playlist_item['snippet']['title'])
        video[FIELD_DESC] = _Encode(playlist_item['snippet']['description'])
        video[FIELD_EVENT] = event_tag
        video[FIELD_VIEW_COUNT] = 0
        video[FIELD_SUBTITLE] = video[FIELD_TITLE]
        video[FIELD_DURATION] = 0
        video[FIELD_SPEAKERS] = ''
        video[FIELD_VIDEO_ID] = (
            playlist_item['snippet']['resourceId']['videoId'])
        video_ids.append(video[FIELD_VIDEO_ID])
        video[FIELD_PUB_DATE] = (playlist_item['snippet']['publishedAt'])
        videos.append(video)

      durations = self._ListVideoDurations(video_ids)
      for v in videos:
        # If we found the video in the playlist but could not retrieve
        # its duration, it's likely been deleted (but not removed from
        # the playlist.
        if v[FIELD_VIDEO_ID] in durations:
          v[FIELD_DURATION] = (durations[v[FIELD_VIDEO_ID]])
          results.append(v)

      # Next batch of videos.
      request = self._NextListRequest(request, response)

    return results


def _AppendYouTubeMetadata(file_path, yt_metadata_rows):
  # Open for append - create if not existing.
  with open(file_path, 'at') as f:
    writer = csv.DictWriter(f, FIELDS)
    # We don't write a header.
    try:
      writer.writerows(yt_metadata_rows)
    except UnicodeEncodeError as e:
      print('UnicodeEncodeError: %s' % e)
  return len(yt_metadata_rows)


def main(argv):
  flags = _ParseFlags(argv)

  data_file = tempfile.mkstemp(suffix='.csv', prefix='yt_meta')[1]

  youtube_service = YTPlaylistService(flags.dev_key)

  rows_written = 0
  for category, playlist_id in _EVENTS:
    rows_written += _AppendYouTubeMetadata(
        data_file,
        yt_metadata_rows=youtube_service.GetPlaylistMetadata(
            playlist_id, category))
  print('Created %s with %d rows.' % (data_file, rows_written))


if __name__ == '__main__':
  main(sys.argv[1:])
