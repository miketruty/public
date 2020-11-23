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
""" Contains 'helper' classes for managing search.Documents.
BaseDocumentManager provides some common utilities, and the Video subclass
adds some Video-document-specific helper methods.
"""

import collections
import copy
import datetime
import logging
import re
import string
import urllib

import categories
import config
import errors
import models
import utils

from google.appengine.api import search
from google.appengine.ext import ndb


class BaseDocumentManager(object):
  """Abstract class. Provides helper methods to manage search.Documents."""

  _INDEX_NAME = None
  _VISIBLE_PRINTABLE_ASCII = frozenset(
      set(string.printable) - set(string.whitespace))

  def __init__(self, doc):
    """Builds a dict of the fields mapped against the field names, for
    efficient access.
    """
    self.doc = doc

  def getFieldVal(self, fname):
    """Get the value of the document field with the given name.  If there is
    more than one such field, the method returns None."""
    try:
      return self.doc.field(fname).value
    except ValueError:
      return None

  def setFirstField(self, new_field):
    """Set the value of the (first) document field with the given name."""
    for i, field in enumerate(self.doc.fields):
      if field.name == new_field.name:
        self.doc.fields[i] = new_field
        return True
    return False

  @classmethod
  def isValidDocId(cls, doc_id):
    """Checks if the given id is a visible printable ASCII string not starting
    with '!'.  Whitespace characters are excluded.
    """
    for char in doc_id:
      if char not in cls._VISIBLE_PRINTABLE_ASCII:
        return False
    return not doc_id.startswith('!')

  @classmethod
  def getIndex(cls):
    return search.Index(name=cls._INDEX_NAME)

  @classmethod
  def deleteAllInIndex(cls):
    """Delete all the docs in the given index."""
    docindex = cls.getIndex()

    try:
      while True:
        # until no more documents, get a list of documents,
        # constraining the returned objects to contain only the doc ids,
        # extract the doc ids, and delete the docs.
        document_ids = [
            document.doc_id for document in docindex.get_range(ids_only=True)
        ]
        if not document_ids:
          break
        docindex.delete(document_ids)
    except search.Error:
      logging.exception('Error removing documents:')

  @classmethod
  def getDoc(cls, doc_id):
    """Return the document with the given doc id. One way to do this is via
    the get_range method, as shown here.  If the doc id is not in the
    index, the first doc in the index will be returned instead, so we need
    to check for that case."""
    if not doc_id:
      return None
    try:
      index = cls.getIndex()
      response = index.get_range(
          start_id=doc_id, limit=1, include_start_object=True)
      if response.results and response.results[0].doc_id == doc_id:
        return response.results[0]
      return None
    except search.InvalidRequest:  # catches ill-formed doc ids
      return None

  @classmethod
  def removeDocById(cls, doc_id):
    """Remove the doc with the given doc id."""
    try:
      cls.getIndex().delete(doc_id)
    except search.Error:
      logging.exception('Error removing doc id %s.', doc_id)

  @classmethod
  def add(cls, documents):
    """wrapper for search index add method; specifies the index name."""
    try:
      return cls.getIndex().put(documents)
    except search.Error:
      logging.exception('Error adding documents.')


def Readable(header_string):
  return header_string.lower().replace('_', ' ')


def ScrubTags(candidate):
  return re.sub(r'<[^>]*?>', '', candidate)


def ScrubDescription(description):
  description = ScrubTags(description)
  fluff = [
      'Missed the conference?',
      'Watch all the talks here: https://goo.gl/c1Vs3h',
      'Watch more talks about Big Data & Machine Learning here:',
      'https://goo.gl/OcqI9k',
      'Watch more talks about Infrastructure & Operations here:',
      'https://goo.gl/k2LOYG',
      'Watch more talks about Collaboration & Productivity here:',
      'https://goo.gl/q3WbLc',
      'Watch more talks about Connected Business Platform here:',
      'https://goo.gl/CtHNJm',
      'Watch more talks about Mobility & Devices here:',
      'https://goo.gl/yl1EqP',
      'Watch more talks about Application Development here:',
      'https://goo.gl/YFgZpl',
  ]
  for f in fluff:
    description = description.replace(f, '')
  return description


def ScrubSpeakers(speakers):
  return ScrubTags(speakers)


class Video(BaseDocumentManager):
  """Provides helper methods to manage Video documents.  All Video documents
  built using these methods will include a core set of fields (see the
  _buildCoreVideoFields method).  We use the given video id (the Video
  entity key) as the doc_id.  This is not required for the entity/document
  design-- each explicitly point to each other, allowing their ids to be
  decoupled-- but using the video id as the doc id allows a document to be
  reindexed given its video info, without having to fetch the
  existing document."""

  _INDEX_NAME = config.VIDEO_INDEX_NAME

  # 'core' video document field names
  UNIQUEID = config.FIELD_UNIQUE_ID
  TITLE = config.FIELD_TITLE
  CATEGORY = config.FIELD_EVENT
  SUBTITLE = config.FIELD_SUBTITLE
  DURATION_MIN = config.FIELD_DURATION
  SPEAKERS = config.FIELD_SPEAKERS
  DESCRIPTION = config.FIELD_DESC
  PUBLISHED_DATE = config.FIELD_PUB_DATE
  SLIDES_LINK = config.FIELD_SLIDES_LINK
  VIEWS = config.FIELD_VIEW_COUNT
  TAGS = config.FIELD_TAGS
  IMAGE = config.FIELD_IMAGE
  VID = config.FIELD_VIDEO_ID
  SESSIONID = config.FIELD_SESSION_ID

  AVG_RATING = 'ar'  #average rating
  UPDATED = 'modified'

  _SORT_OPTIONS = [
      [
          #     AVG_RATING, 'average rating', search.SortExpression(
          #         expression=AVG_RATING,
          #         direction=search.SortExpression.DESCENDING,
          #         default_value=0)
          # ], [
          VIEWS,
          Readable(VIEWS),
          search.SortExpression(
              expression=VIEWS,
              direction=search.SortExpression.DESCENDING,
              default_value=0)
      ],
      [
          DURATION_MIN, Readable(DURATION_MIN), search.SortExpression(
              expression=DURATION_MIN,
              direction=search.SortExpression.ASCENDING,
              default_value=9999)
      ],
      [
          PUBLISHED_DATE, Readable(PUBLISHED_DATE), search.SortExpression(
              expression=PUBLISHED_DATE,
              direction=search.SortExpression.DESCENDING,
              default_value=1)
      ],
      [
          #     UPDATED, Readable(UPDATED), search.SortExpression(
          #         expression=UPDATED,
          #         direction=search.SortExpression.DESCENDING,
          #         default_value=1)
          # ], [
          CATEGORY,
          Readable(CATEGORY),
          search.SortExpression(
              expression=CATEGORY,
              direction=search.SortExpression.ASCENDING,
              default_value='')
      ],
      [
          TITLE, Readable(TITLE), search.SortExpression(
              expression=TITLE,
              direction=search.SortExpression.ASCENDING,
              default_value='zzz')
      ]
  ]

  _SORT_MENU = None
  _SORT_DICT = None

  @classmethod
  def deleteAllInVideoIndex(cls):
    cls.deleteAllInIndex()

  @classmethod
  def getSortMenu(cls):
    if not cls._SORT_MENU:
      cls._buildSortMenu()
    return cls._SORT_MENU

  @classmethod
  def getSortDict(cls):
    if not cls._SORT_DICT:
      cls._buildSortDict()
    return cls._SORT_DICT

  @classmethod
  def _buildSortMenu(cls):
    """Build the default set of sort options used for Video search.
    Of these options, all but 'relevance' reference core fields that
    all Videos will have."""
    res = [(elt[0], elt[1]) for elt in cls._SORT_OPTIONS]
    cls._SORT_MENU = [('relevance', 'relevance')] + res

  @classmethod
  def _buildSortDict(cls):
    """Build a dict that maps sort option keywords to their corresponding
    SortExpressions."""
    cls._SORT_DICT = {}
    for elt in cls._SORT_OPTIONS:
      cls._SORT_DICT[elt[0]] = elt[2]

  @classmethod
  def getDocFromUid(cls, uid):
    """Given a uid, get its doc. We're using the uid as the doc id, so we can
    do this via a direct fetch."""
    return cls.getDoc(uid)

  @classmethod
  def removeVideoDocByUid(cls, uid):
    """Given a doc's vid, remove the doc matching it from the video
    index."""
    cls.removeDocById(uid)

  @classmethod
  def updateRatingInDoc(cls, doc_id, avg_rating):
    # get the associated doc from the doc id in the video entity
    doc = cls.getDoc(doc_id)
    if doc:
      pdoc = cls(doc)
      pdoc.setAvgRating(avg_rating)
      # The use of the same id will cause the existing doc to be reindexed.
      return doc
    else:
      raise errors.OperationFailedError(
          'Could not retrieve doc associated with id %s' % (doc_id,))

  @classmethod
  def updateRatingsInfo(cls, doc_id, avg_rating):
    """Given a models.Video entity, update and reindex the associated
    document with the video entity's current average rating. """

    ndoc = cls.updateRatingInDoc(doc_id, avg_rating)
    # reindex the returned updated doc
    return cls.add(ndoc)

# 'accessor' convenience methods

  def getUniqueID(self):
    """Get the value of the 'uniqueid' field of a Video doc."""
    return self.getFieldVal(self.UNIQUEID)

  def getTitle(self):
    """Get the value of the 'title' field of a Video doc."""
    return self.getFieldVal(self.TITLE)

  def getCategory(self):
    """Get the value of the 'cat' field of a Video doc."""
    return self.getFieldVal(self.CATEGORY)

  def setCategory(self, cat):
    """Set the value of the 'cat' (category) field of a Video doc."""
    return self.setFirstField(search.NumberField(name=self.CATEGORY, value=cat))

  def getSlidesLink(self):
    """Get the value of the 'slides_link' field of a Video doc."""
    return self.getFieldVal(self.SLIDES_LINK)

  def getSubtitle(self):
    """Get the value of the 'sutitle' field of a Video doc."""
    return self.getFieldVal(self.SUBTITLE)

  def getDurationMin(self):
    """Get the value of the 'duration_min' field of a Video doc."""
    return self.getFieldVal(self.DURATION_MIN)

  def getSpeakers(self):
    """Get the value of the 'speakers' field of a Video doc."""
    return self.getFieldVal(self.SPEAKERS)

  def getDescription(self):
    """Get the value of the 'description' field of a Video doc."""
    return self.getFieldVal(self.DESCRIPTION)

  def getPublishedDate(self):
    """Get the value of the 'published_date' field of a Video doc."""
    return self.getFieldVal(self.PUBLISHED_DATE)

  def getViews(self):
    """Get the value of the 'views' field of a Video doc."""
    return self.getFieldVal(self.VIEWS)

  def getTags(self):
    """Get the value of the 'tags' field of a Video doc."""
    return self.getFieldVal(self.TAGS)

  def getImage(self):
    """Get the value of the 'image' field of a Video doc."""
    return self.getFieldVal(self.IMAGE)

  def getVID(self):
    """Get the value of the 'vid' field of a Video doc."""
    return self.getFieldVal(self.VID)

  def getSessionID(self):
    """Get the value of the 'sessionid' field of a Video doc."""
    return self.getFieldVal(self.SESSIONID)

  def getAvgRating(self):
    """Get the value of the 'ar' (average rating) field of a Video doc."""
    return self.getFieldVal(self.AVG_RATING)

  def setAvgRating(self, ar):
    """Set the value of the 'ar' field of a Video doc."""
    return self.setFirstField(
        search.NumberField(name=self.AVG_RATING, value=ar))

  @classmethod
  def generateRatingsBuckets(cls, query_string):
    """Builds a dict of ratings 'buckets' and their counts, based on the
    value of the 'avg_rating" field for the documents retrieved by the given
    query.  See the 'generateRatingsLinks' method.  This information will
    be used to generate sidebar links that allow the user to drill down in query
    results based on rating.

    For demonstration purposes only; this will be expensive for large data
    sets.
    """

    # do the query on the *full* search results
    # to generate the facet information, imitating what may in future be
    # provided by the FTS API.
    try:
      sq = search.Query(query_string=query_string.strip())
      search_results = cls.getIndex().search(sq)
    except search.Error:
      logging.exception('An error occurred on search.')
      return None

    ratings_buckets = collections.defaultdict(int)
    # populate the buckets
    for res in search_results:
      ratings_buckets[int((cls(res)).getAvgRating() or 0)] += 1
    return ratings_buckets

  @classmethod
  def generateRatingsLinks(cls, query, vhash):
    """Given a dict of ratings 'buckets' and their counts,
    builds a list of html snippets, to be displayed in the sidebar when
    showing results of a query. Each is a link that runs the query, additionally
    filtered by the indicated ratings interval."""

    ratings_buckets = cls.generateRatingsBuckets(query)
    if not ratings_buckets:
      return None
    rlist = []
    for k in range(config.RATING_MIN, config.RATING_MAX + 1):
      try:
        v = ratings_buckets[k]
      except KeyError:
        return
      # build html
      if k < 5:
        htext = '%s-%s (%s)' % (k, k + 1, v)
      else:
        htext = '%s (%s)' % (k, v)
      vhash['rating'] = k
      hlink = '/vsearch?' + urllib.urlencode(vhash)
      rlist.append((hlink, htext))
    return rlist

  @classmethod
  def _buildCoreVideoFields(cls, unique_id, title, category, subtitle,
                            duration_min, speakers, description,
                            published_date, views, slides_link, tags, image,
                            video_id, session_id):
    """Construct a 'core' document field list for the fields common to all
    Videos. The various categories (as defined in the file 'categories.py'),
    may add additional specialized fields; these will be appended to this
    core list. (see _buildVideoFields)."""
    fields = [
        search.TextField(name=cls.UNIQUEID, value=unique_id),
        # The 'updated' field is always set to the current date.
        search.DateField(
            name=cls.UPDATED, value=datetime.datetime.now().date()),
        search.TextField(name=cls.TITLE, value=title),
        search.AtomField(name=cls.CATEGORY, value=category),
        search.TextField(name=cls.SUBTITLE, value=subtitle),
        search.NumberField(name=cls.DURATION_MIN, value=int(duration_min)),
        search.TextField(name=cls.SPEAKERS, value=ScrubSpeakers(speakers)),
        # strip the markup from the description value, which can
        # potentially come from user input.  We do this so that
        # we don't need to sanitize the description in the
        # templates, showing off the Search API's ability to mark up query
        # terms in generated snippets.  This is done only for
        # demonstration purposes; in an actual app,
        # it would be preferrable to use a library like Beautiful Soup
        # instead.
        # We'll let the templating library escape all other rendered
        # values for us, so this is the only field we do this for.
        search.TextField(
            name=cls.DESCRIPTION, value=ScrubDescription(description)),
        search.NumberField(name=cls.VIEWS, value=int(views)),
        search.TextField(name=cls.SLIDES_LINK, value=slides_link),
        search.TextField(name=cls.TAGS, value=tags),
        search.TextField(name=cls.IMAGE, value=image),
        search.TextField(name=cls.VID, value=video_id),
        search.TextField(name=cls.SESSIONID, value=session_id),
        search.NumberField(name=cls.AVG_RATING, value=0.0),
    ]
    # Some fields can sometimes be empty.
    scrubbed_publish_date = utils.dateFromDateString(published_date)
    if scrubbed_publish_date:
      fields.append(search.DateField(
          name=cls.PUBLISHED_DATE, value=scrubbed_publish_date))
    return fields

  @classmethod
  def _buildVideoFields(cls, unique_id, category, title, category_name,
                        subtitle, duration_min, speakers, description,
                        published_date, views, slides_link, tags, image,
                        video_id, session_id, **params):
    """Build all the additional non-core fields for a document of the given
    video type (category), using the given params dict, and the
    already-constructed list of 'core' fields.  All such additional
    category-specific fields are treated as required.
    """
    fields = cls._buildCoreVideoFields(
        unique_id, title, category, subtitle, duration_min, speakers,
        description, published_date, views, slides_link, tags, image, video_id,
        session_id)
    # get the specification of additional (non-'core') fields for this category
    vdict = categories.event_dict.get(category_name)
    if vdict:
      # for all fields
      for k, field_type in vdict.iteritems():
        # see if there is a value in the given params for that field.
        # if there is, get the field type, create the field, and append to the
        # document field list.
        if k in params:
          v = params[k]
          if field_type == search.NumberField:
            try:
              val = float(v)
              fields.append(search.NumberField(name=k, value=val))
            except ValueError:
              error_message = ('bad value %s for field %s of type %s' %
                               (k, v, field_type))
              logging.error(error_message)
              raise errors.OperationFailedError(error_message)
          elif field_type == search.TextField:
            fields.append(search.TextField(name=k, value=str(v)))
          else:
            # you may want to add handling of other field types for generality.
            # Not needed for our current sample data.
            logging.warn('not processed: %s, %s, of type %s', k, v, field_type)
        else:
          error_message = ('value not given for field "%s" of field type "%s"' %
                           (k, field_type))
          logging.warn(error_message)
          raise errors.OperationFailedError(error_message)
    #else:
    #  # else, did not have an entry in the params dict for the given field.
    #  logging.warn(
    #      'video field information not found for category name %s',
    #      params['category_name'])
    return fields

  @classmethod
  def _createDocument(cls,
                      unique_id=None,
                      event=None,
                      title=None,
                      category_name=None,
                      subtitle=None,
                      duration_min=None,
                      speakers=None,
                      description=None,
                      published_date=None,
                      views=None,
                      slides_link=None,
                      tags=None,
                      image=None,
                      video_id=None,
                      session_id=None,
                      **params):
    """Create a Document object from given params."""
    # check for the fields that are always required.
    if unique_id and event and title:
      # First, check that the given unique_id has only visible ascii characters,
      # and does not contain whitespace.  The unique_id will be used as the
      # doc_id, which has these requirements.
      if not cls.isValidDocId(unique_id):
        raise errors.OperationFailedError('Illegal unique_id %s' % unique_id)
      # construct the document fields from the params
      resfields = cls._buildVideoFields(
          unique_id=unique_id,
          category=event,
          title=title,
          category_name=category_name,
          subtitle=subtitle,
          duration_min=duration_min,
          speakers=speakers,
          description=description,
          published_date=published_date,
          views=views,
          slides_link=slides_link,
          tags=tags,
          image=image,
          video_id=video_id,
          session_id=session_id,
          **params)
      # build and index the document.  Use the video_id as the doc id.
      # (If we did not do this, and left the doc_id unspecified, an id would be
      # auto-generated.)
      d = search.Document(doc_id=unique_id, fields=resfields)
      return d
    else:
      raise errors.OperationFailedError('Missing parameter.')

  @classmethod
  def _normalizeParams(cls, params):
    """Normalize the submitted params for building a video."""
    params = copy.deepcopy(params)
    try:
      params[cls.UNIQUEID] = params[cls.UNIQUEID].strip()
      params[cls.TITLE] = params[cls.TITLE].strip()
      params['category_name'] = params[cls.CATEGORY]
      params[cls.CATEGORY] = params[cls.CATEGORY]
      if params[cls.SUBTITLE]:
        params[cls.SUBTITLE] = params[cls.SUBTITLE].strip()
      if params[cls.SPEAKERS]:
        params[cls.SPEAKERS] = params[cls.SPEAKERS].strip()
      if params[cls.SLIDES_LINK]:
        params[cls.SLIDES_LINK] = params[cls.SLIDES_LINK].strip()
      try:
        params[cls.DURATION_MIN] = int(params[cls.DURATION_MIN])
      except (ValueError, TypeError):
        error_message = 'bad duration_min value: %s' % params[cls.DURATION_MIN]
        logging.error(error_message)
        raise errors.OperationFailedError(error_message)
      try:
        params[cls.VIEWS] = int(params[cls.VIEWS])
      except ValueError:
        error_message = 'bad views value: %s' % params[cls.VIEWS]
        logging.error(error_message)
        raise errors.OperationFailedError(error_message)
      if params[cls.TAGS]:
        params[cls.TAGS] = params[cls.TAGS].strip()
      if params[cls.IMAGE]:
        params[cls.IMAGE] = params[cls.IMAGE].strip()
      if params[cls.VID]:
        params[cls.VID] = params[cls.VID].strip()
      if params[cls.SESSIONID]:
        params[cls.SESSIONID] = params[cls.SESSIONID].strip()
      return params
    except KeyError as e1:
      logging.exception('key error')
      raise errors.OperationFailedError(e1)
    except errors.Error as e2:
      logging.debug('Problem with params: %s: %s', params, e2.error_message)
      raise errors.OperationFailedError(e2.error_message)

  @classmethod
  def buildVideoBatch(cls, rows):
    """Build video documents and their related datastore entities, in batch,
    given a list of params dicts.  Should be used for new videos, as does not
    handle updates of existing video entities. This method does not require
    that the doc ids be tied to the video ids, and obtains the doc ids from
    the results of the document add."""
    docs = []
    dbps = []
    for row in rows:
      try:
        params = cls._normalizeParams(row)
        doc = cls._createDocument(**params)
        docs.append(doc)
        # create video entity, sans doc_id
        dbp = models.Video(
            id=params[cls.UNIQUEID],
            duration_min=int(params[cls.DURATION_MIN]),
            category=params[cls.CATEGORY])
        dbps.append(dbp)
      except errors.OperationFailedError:
        logging.error('error creating document from data: %s.', row)
    logging.debug('buildVideoBatch: docs=%s.', len(docs))
    logging.debug('buildVideoBatch: dbps=%s.', len(dbps))
    try:
      add_results = cls.add(docs)
    except search.Error:
      logging.exception('Add failed')
      return
    if len(add_results) != len(dbps):
      # this case should not be reached; if there was an issue,
      # search.Error should have been thrown, above.
      raise errors.OperationFailedError(
          'Error: wrong number of results returned from indexing operation')
    # now set the entities with the doc ids, the list of which are returned in
    # the same order as the list of docs given to the indexers
    for i, dbp in enumerate(dbps):
      dbp.doc_id = add_results[i].id
    # persist the entities
    ndb.put_multi(dbps)

  @classmethod
  def buildVideo(cls, params):
    """Create/update a video document and its related datastore entity.  The
    video id and the field values are taken from the params dict.
    """
    params = cls._normalizeParams(params)
    # check to see if doc already exists.  We do this because we need to retain
    # some information from the existing doc.  We could skip the fetch if this
    # were not the case.
    curr_doc = cls.getDocFromUid(params[cls.UNIQUEID])
    d = cls._createDocument(**params)
    if curr_doc:  #  retain ratings info from existing doc
      avg_rating = cls(curr_doc).getAvgRating()
      cls(d).setAvgRating(avg_rating)

    # This will reindex if a doc with that doc id already exists
    doc_ids = cls.add(d)
    try:
      doc_id = doc_ids[0].id
    except IndexError:
      doc_id = None
      raise errors.OperationFailedError('could not index document')
    logging.debug('got new doc id %s for video: %s', doc_id, params[cls.UNIQUEID])

    # now update the entity
    def _tx():
      # Check whether the video entity exists. If so, we want to update
      # from the params, but preserve its ratings-related info.
      v = models.Video.get_by_id(params[cls.UNIQUEID])
      if v:  #update
        v.update_core(params, doc_id)
      else:  # create new entity
        v = models.Video.create(params, doc_id)
      v.put()
      return v

    v = ndb.transaction(_tx)
    logging.debug('video: %s', v)
    return v
