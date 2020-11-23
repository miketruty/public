#!/usr/bin/env python
#
# Copyright 2017 Google Inc.
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

"""Contains the handlers that require administrative access."""

import csv
import difflib
import logging
import os
import pprint
import urllib
import uuid

from base_handler import BaseHandler
import categories
import config
import docs
import errors
import models
import utils
import youtube_service

import cloudstorage as gcs
from google.appengine.api import app_identity
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb

BUCKET_NAME = os.environ.get('BUCKET_NAME',
                             app_identity.get_default_gcs_bucket_name())
DATAFILE = '/%s' % os.path.join(BUCKET_NAME, config.VIDEO_DATA)

_DIFFER = difflib.Differ()
_ENCODING = 'utf-8'

gcs.set_default_retry_params(
    gcs.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=
        15))


class PubSubHandler(BaseHandler):
  """Handle PubSub notifications."""

  def post(self):
    """Handle when the metadata file is updated."""
    # TODO(truty): because of IAP need to re-write this to be a cron
    # handler doing pubsub pull.
    # https://cloud.google.com/appengine/docs/flexible/python/writing-and-responding-to-pub-sub-messages
    if self.request.get('token') != config.PUBSUB_VERIFICATION_TOKEN:
      self.error(400)

    # Now we can reinit.
    # _ReinitAll()


def _ReinitAll(video_data=True):
  """Deletes all video entities and documents.

  Essentially resetting the app state, then loads in static data if requested.

  Hardwired for the expected video types in the data. This function
  is intended to be run 'offline' (e.g., via a Task Queue task). As an
  extension to this functionality, the channel ID could be used to notify
  when done.
  """

  # delete all the video and review entities
  review_keys = models.Review.query().fetch(keys_only=True)
  ndb.delete_multi(review_keys)
  vid_keys = models.Video.query().fetch(keys_only=True)
  ndb.delete_multi(vid_keys)
  # delete all the associated product documents in the doc
  docs.Video.deleteAllInVideoIndex()
  logging.info('All deleted.')
  # load in data if indicated
  if video_data:
    logging.info('Loading video data')
    datafile = os.path.join('data', config.VIDEO_DATA)
    if os.path.exists(datafile):
      # For dev_appserver avoid bucket, supposed to work, but does not.
      logging.info('******Using LOCAL video data...')
      with open(datafile, 'r') as f:
        reader = csv.DictReader(f, config.FIELDS)
        _ImportDataToSearch(reader)
    else:
      # Live App Engine reads from GCS bucket.
      with gcs.open(DATAFILE, 'r') as gcs_data_file:
        reader = csv.DictReader(iter(gcs_data_file.readline, ''), config.FIELDS)
        _ImportDataToSearch(reader)
  logging.info('Re-initialization complete.')


def _BuildVideoBatch(videos, yt_service):
  """Send the videos to the docs video builder.

  Get view counts first.
  """
  logging.debug('BuildVideoBatch: %s entities.', len(videos))
  video_ids = [
      v[config.FIELD_VIDEO_ID] for v in videos
      if v[config.FIELD_EVENT] in categories.YOUTUBE_CATS]
  logging.debug('BuildVideoBatch: %s YouTube videos of %s total docs.',
                len(video_ids), len(videos))

  video_counts = yt_service.ListVideos(video_ids)
  for v in videos:
    vid = v[config.FIELD_VIDEO_ID]
    count = video_counts.get(vid, 0)
    if count:
      v[config.FIELD_VIEW_COUNT] = count

  docs.Video.buildVideoBatch(videos)


def _ImportDataToSearch(reader):
  """Import via the csv reader iterator.

  Using the specified batch size as set in the config file.
  We want to ensure the batch is not too large-- we allow 100
  rows/products max per batch.
  """
  total_rows_imported = 0
  max_batch_size = 100
  rows = []
  # index in batches
  # ensure the batch size in the config file is not over the max or < 1.
  batchsize = utils.intClamp(config.IMPORT_BATCH_SIZE, 1, max_batch_size)
  logging.debug('batchsize: %s', batchsize)

  yt_service = youtube_service.YTStatisticsService()
  for row in reader:
    if len(rows) == batchsize:
      _BuildVideoBatch(rows, yt_service)
      rows = []

    rows.append(row)
    total_rows_imported += 1

  if rows:
    _BuildVideoBatch(rows, yt_service)

  logging.debug('Total rows imported: %s.', total_rows_imported)


class AdminHandler(BaseHandler):
  """Displays the admin page."""

  def buildAdminPage(self, notification=None):
    # If necessary, build the app's video/event categories now.  This is done
    # only if there are no Category entities in the datastore.
    models.Category.buildAllCategories()
    tdict = {
        'datafile': DATAFILE,
        #         'update_sample': config.DEMO_UPDATE_BOOKS_DATA,
    }
    if notification:
      tdict['notification'] = notification
    self.render_template('admin.html', tdict)

  @BaseHandler.logged_in
  def get(self):
    action = self.request.get('action')
    if action == 'reinit':
      # reinitialise the app data to the sample data
      defer(_ReinitAll)
      self.buildAdminPage(notification='Reinitialization performed.')

    # elif action == 'demo_update':
    #   # update the sample data, from (hardwired) update data. Demonstrates
    #   # updating some existing products, and adding some new ones.
    #   logging.info('Loading sample update data')
    #   # The following is hardwired to the known format of the sample data file
    #   # TODO: fix update case.
    #   datafile = os.path.join('data', config.DEMO_UPDATE_BOOKS_DATA)
    #   reader = csv.DictReader(
    #       open(datafile, 'r'), [
    #           'pid', 'name', 'category', 'price', 'publisher', 'title',
    #           'pages',
    #           'author', 'description', 'isbn'
    #       ])
    #   for row in reader:
    #     docs.Video.buildVideo(row)
    #   self.buildAdminPage(notification='Demo update performed.')

    elif action == 'update_ratings':
      self.update_ratings()
      self.buildAdminPage(notification='Ratings update performed.')
    else:
      self.buildAdminPage()

  def update_ratings(self):
    """Find the videos that have had an average ratings change.

    And that need their associated documents updated (re-indexed) to
    reflect that change; and re-index those docs in batch. There will only
    be such products if config.BATCH_RATINGS_UPDATE is True; otherwise the
    associated documents will be updated right away.
    """
    # get the vids of the videos that need review info updated in their
    # associated documents.
    vkeys = models.Video.query(models.Video.needs_review_reindex == True).fetch(
        keys_only=True)
    # re-index these docs in batch
    models.Video.updateVideoDocsWithNewRating(vkeys)


def _FixNewlines(string_field):
  if isinstance(string_field, str):
    result = string_field.replace('    ', ' ')
    result = result.replace('   ', ' ')
    result = result.replace('  ', ' ')
    result = result.replace('   \n\n', '\n\n')
    result = result.replace('  \n\n', '\n\n')
    result = result.replace(' \n\n', '\n\n')
    result = result.replace('   \\n\\n', '\\n\\n')
    result = result.replace('  \\n\\n', '\\n\\n')
    result = result.replace(' \\n\\n', '\\n\\n')
    return result
  return string_field


def _StrToUnicode(string_field):
  # Convert to Unicde.
  if isinstance(string_field, str):
    return string_field.decode(_ENCODING, 'replace')
  return string_field


def _UnicodeToStr(unicode_field):
  # Convert to str
  if isinstance(unicode_field, unicode):
    result = unicode_field.replace(u'\u0107', u'c')  # c acute
    result = result.replace(u'\u0142', u'l')  # l stroke
    result = result.replace(u'\xe9', u'e')  # e acute
    result = result.replace(u'\xf6', u'o')  # o umlaut
    result = result.replace(u'\u2013', u'-')
    result = result.replace(u'\u2014', u'-')
    result = result.replace(u'\u2018', u"'")
    result = result.replace(u'\u2019', u"'")
    result = result.replace(u'\u201c', u'"')
    result = result.replace(u'\u201d', u'"')
    result = result.encode('ascii', 'strict')
  else:
    result = unicode_field
  return result.strip()


def _SafeString(string_field):
  return _FixNewlines(_UnicodeToStr(_StrToUnicode(string_field)))


def _ShowDiff(field1, field2):
  return pprint.pformat(
      list(_DIFFER.compare([field1], [field2])), indent=2, width=40)


def _RetrieveAllMetadata(reader):
  # Get metadata both from the master file and YouTube.
  metadata = {}
  speakers_count = 0
  for r in reader:
    speakers = _StrToUnicode(r[config.FIELD_SPEAKERS])
    if speakers:
      speakers_count += 1
    metadata[r[config.FIELD_VIDEO_ID]] = {
        config.FIELD_TITLE: _SafeString(r[config.FIELD_TITLE]),
        config.FIELD_DESC: _SafeString(r[config.FIELD_DESC]),
        config.FIELD_SPEAKERS: speakers
    }

  yt_service = youtube_service.YTSnippetService()
  yt_results = yt_service.ListVideos(sorted(
      k for k, v in metadata.iteritems()
      if v[config.FIELD_EVENT] in categories.YOUTUBE_CATS))

  # Compare, only show differences
  yt_count = 0
  same_title_count = 0
  same_desc_count = 0
  errors = []
  for video_id, yt_dict in yt_results.iteritems():
    yt_count += 1
    if video_id not in metadata:
      errors.append('%s not in metadata!.' % video_id)
      continue

    yt_title = _SafeString(yt_dict[config.FIELD_TITLE])
    if metadata[video_id][config.FIELD_TITLE] == yt_title:
      same_title_count += 1
      del metadata[video_id][config.FIELD_TITLE]
    else:
      yt_key = '%s_%s' % (config.FIELD_TITLE, config.FIELD_YOUTUBE)
      metadata[video_id][yt_key] = (yt_title, _ShowDiff(
          yt_title, metadata[video_id][config.FIELD_TITLE]))

    yt_desc = _SafeString(yt_dict[config.FIELD_DESC])
    if metadata[video_id][config.FIELD_DESC] == yt_desc:
      same_desc_count += 1
      del metadata[video_id][config.FIELD_DESC]
      if config.FIELD_TITLE not in metadata[video_id]:
        if ((config.FIELD_SPEAKERS in metadata[video_id]) and
            (not metadata[video_id][config.FIELD_SPEAKERS])):
          del metadata[video_id][config.FIELD_SPEAKERS]
        if config.FIELD_SPEAKERS not in metadata[video_id]:
          del metadata[video_id]
    else:
      yt_key = '%s_%s' % (config.FIELD_DESC, config.FIELD_YOUTUBE)
      metadata[video_id][yt_key] = (yt_desc, _ShowDiff(
          yt_desc, metadata[video_id][config.FIELD_DESC]))

  stats = [yt_count, same_title_count, same_desc_count, speakers_count]
  return metadata, errors, stats


def RetrieveMetadata():
  datafile = os.path.join('data', config.VIDEO_DATA)
  if os.path.exists(datafile):
    # For dev_appserver avoid bucket, supposed to work, but does not.
    with open(datafile, 'r') as f:
      reader = csv.DictReader(f, config.FIELDS)
      return _RetrieveAllMetadata(reader)
  # Live App Engine reads from GCS bucket.
  with gcs.open(DATAFILE, 'r') as gcs_data_file:
    reader = csv.DictReader(iter(gcs_data_file.readline, ''), config.FIELDS)
    return _RetrieveAllMetadata(reader)


class MetaDiffHandler(BaseHandler):
  """Displays a report of metadata differences page."""

  @BaseHandler.logged_in
  def get(self):
    metadata, errors, stats = RetrieveMetadata()
    tdict = {'metadata': metadata, 'errors': errors, 'stats': stats}
    self.render_template('metadiff.html', tdict)


class DeleteVideoHandler(BaseHandler):
  """Remove data for the video with the given pid, including that video's
  reviews and its associated indexed document."""

  @BaseHandler.logged_in
  def post(self):
    vid = self.request.get('vid')
    if not vid:  # this should not be reached
      msg = 'There was a problem: no video id given.'
      logging.error(msg)
      url = '/'
      linktext = 'Go to video search page.'
      self.render_template('notification.html', {
          'title': 'Error',
          'msg': msg,
          'goto_url': url,
          'linktext': linktext
      })
      return

    # Delete the video entity within a transaction, and define transactional
    # tasks for deleting the video's reviews and its associated document.
    # These tasks will only be run if the transaction successfully commits.
    def _tx():
      v = models.Video.get_by_id(vid)
      if v:
        v.key.delete()
        defer(models.Review.deleteReviews, v.key.id(), _transactional=True)
        defer(docs.Video.removeVideoDocByUid, v.key.id(), _transactional=True)

    ndb.transaction(_tx)
    # indicate success
    msg = ('The video with video id %s has been ' + 'successfully removed.') % (
        vid,)
    url = '/'
    linktext = 'Go to video search page.'
    self.render_template('notification.html', {
        'title': 'Video Removed',
        'msg': msg,
        'goto_url': url,
        'linktext': linktext
    })


class CreateVideoHandler(BaseHandler):
  """Handler to create a new video: this constitutes both a video entity
  and its associated indexed document."""

  def parseParams(self):
    """Filter the param set to the expected params."""

    vid = self.request.get('vid')
    doc = docs.Video.getDocFromVid(vid)
    params = {}
    if doc:  # populate default params from the doc
      fields = doc.fields
      for f in fields:
        params[f.name] = f.value
    else:
      # start with the 'core' fields, same order we usually render them.
      params = {
          'vid': uuid.uuid4().hex,  # auto-generate default UID
          config.FIELD_VIDEO_ID: '',
          config.FIELD_TITLE: '',
          config.FIELD_EVENT: '',
          config.FIELD_VIEW_COUNT: 0,
          config.FIELD_SUBTITLE: '',
          config.FIELD_DURATION: '',
          config.FIELD_SPEAKERS: '',
          config.FIELD_DESC: '',
          config.FIELD_PUB_DATE: '',
          config.FIELD_SLIDES_LINK: '',
      }
      pf = categories.event_dict
      # add the fields specific to the categories
      for _, cdict in pf.iteritems():
        temp = {}
        for elt in cdict.keys():
          temp[elt] = ''
        params.update(temp)

    for k, v in params.iteritems():
      # Process the request params. Possibly replace default values.
      params[k] = self.request.get(k, v)
    return params

  @BaseHandler.logged_in
  def get(self):
    params = self.parseParams()
    self.render_template('create_video.html', params)

  @BaseHandler.logged_in
  def post(self):
    self.createProduct(self.parseParams())

  def createProduct(self, params):
    """Create a product entity and associated document from the given params
    dict."""

    try:
      product = docs.Video.buildVideo(params)
      self.redirect('/product?' + urllib.urlencode({
          'pid': product.pid,
          'vname': params['name'],
          'category': product.category
      }))
    except errors.Error as e:
      logging.exception('Error:')
      params['error_message'] = e.error_message
      self.render_template('create_video.html', params)
