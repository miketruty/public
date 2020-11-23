# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helpers for interacting with YouTube API."""

import logging

import config

from apiclient.discovery import build

# From gcp-next-reviewdeo
# _API_DEV_KEY = ''

# From google.com:cloud-next-library
# _API_DEV_KEY = ''

# From google.com:truty-goog-com-csa
_API_DEV_KEY = '' # Need this to deploy for real!!

_MAX_RESULTS = 50  # Max possible is 50, default is 5.

_YOUTUBE_API_BATCH = 10  # 10 videos in a batch to add to a playlist
_YOUTUBE_API_SERVICE_NAME = 'youtube'
_YOUTUBE_API_VERSION = 'v3'


def _BuildYouTubeService(credentials=None, dev_key=None):
  return build(
      _YOUTUBE_API_SERVICE_NAME,
      _YOUTUBE_API_VERSION,
      credentials=credentials,
      developerKey=dev_key)


def CreatePlaylist(credentials,
                   playlist_name,
                   description,
                   privacy_status='private'):
  """Creates an EMPTY playlist."""
  # This is not a class so the AddItems call can be deferrable.
  yt = _BuildYouTubeService(credentials=credentials)
  playlists_insert_response = yt.playlists().insert(
      part='snippet,status',
      body=dict(
          snippet=dict(title=playlist_name, description=description),
          status=dict(privacyStatus=privacy_status))).execute()
  return playlists_insert_response['id']


def AddPlaylistItems(credentials, pid, vids):
  """Add items to a playlist."""
  yt = _BuildYouTubeService(credentials=credentials)
  # Would prefer to batch and defer this but YouTube API not yet there.
  for vid in vids:
    playlistitems_insert_response = (yt.playlistItems().insert(
        part='snippet',
        body=dict(snippet=dict(
            playlistId=pid, resourceId=dict(videoId=vid,
                                            kind='youtube#video'))))).execute()
    if not playlistitems_insert_response:
      logging.error('Unexpectedly empty insert response.')


class YTVideoListServiceBase(object):
  """Class for organizing listing of YouTube videos."""

  def __init__(self, dev_key=_API_DEV_KEY):
    self._youtube = _BuildYouTubeService(dev_key=dev_key)

  def _GetItemData(self, item):
    # Override this and return the fields you need from each item.
    item_result = {}
    return item_result.get(item)

  def _ListVideosBatch(self, part, video_ids):
    results = {}
    if (not part) or (not video_ids):
      return results

    video_response = self._youtube.videos().list(
        id=','.join(video_ids), part=part, maxResults=_MAX_RESULTS).execute()
    for item in video_response.get('items', []):
      results[item['id']] = self._GetItemData(item)
    return results

  def _ListVideos(self, part, video_ids):
    # Need to work in batches
    video_count = len(video_ids)
    i = 0
    j = min(video_count, _MAX_RESULTS)

    results = {}

    while i < video_count:
      results.update(self._ListVideosBatch(part, video_ids[i:j]))

      i = j
      j += _MAX_RESULTS
      j = min(j, video_count)

    return results

  def ListVideos(self, video_ids):
    # Override this and pass the part(s) needed.
    part = ''
    return self._ListVideos(part, video_ids)


class YTStatisticsService(YTVideoListServiceBase):

  def _GetItemData(self, item):
    return int(item['statistics']['viewCount'])

  def ListVideos(self, video_ids):
    part = 'statistics'
    return self._ListVideos(part, video_ids)


class YTSnippetService(YTVideoListServiceBase):

  def _GetItemData(self, item):
    return {
        config.FIELD_TITLE: item['snippet'][config.FIELD_TITLE],
        config.FIELD_DESC: item['snippet'][config.FIELD_DESC],
    }

  def ListVideos(self, video_ids):
    part = 'snippet'
    return self._ListVideos(part, video_ids)
