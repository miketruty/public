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
""" Contains the Datastore model classes used by the app: Category, Video,
and Review.
Each Video entity will have a corresponding indexed "video" search.Document.
Video entities contain a subset of the fields in their corresponding document.
Video Review entities are not indexed (do not have corresponding Documents).
Reviews include a video id field, pointing to their 'parent' video, but
are not part of the same entity group, thus avoiding contention in
scenarios where a large number of video reviews might be edited/added at once.
"""

import logging

import categories
import docs

from google.appengine.api import memcache
from google.appengine.ext import ndb


class Category(ndb.Model):
  """The model class for video category information.  Supports building a
  category tree."""

  _CATEGORY_INFO = None
  _CATEGORY_DICT = None
  _RCATEGORY_DICT = None
  _ROOT = 'root'  # the 'root' category of the category tree

  parent_category = ndb.KeyProperty()

  @property
  def category_name(self):
    return self.key.id()

  @classmethod
  def buildAllCategories(cls):
    """ build the category instances from the provided static data, if category
    entities do not already exist in the Datastore. (see categories.py)."""

    # Don't build if there are any categories in the datastore already
    if cls.query().get():
      return
    root_category = categories.ctree
    cls.buildCategory(root_category, None)

  @classmethod
  def buildCategory(cls, category_data, parent_key):
    """build a category and any children from the given data dict."""

    if not category_data:
      return
    cname = category_data.get('name')
    if not cname:
      logging.warn('no category name for %s', category)
      return
    if parent_key:
      cat = cls(id=cname, parent_category=parent_key)
    else:
      cat = cls(id=cname)
    cat.put()

    children = category_data.get('children')
    # if there are any children, build them using their parent key
    cls.buildChildCategories(children, cat.key)

  @classmethod
  def buildChildCategories(cls, children, parent_key):
    """Given a list of category data structures and a parent key, build the
    child categories, with the given key as their entity group parent."""
    for cat in children:
      cls.buildCategory(cat, parent_key)

  @classmethod
  def getCategoryInfo(cls):
    """Build and cache a list of category id/name correspondences.  This info is
    used to populate html select menus."""
    if not cls._CATEGORY_INFO:
      cls.buildAllCategories()  # first build categories from data file
      # if required
      cats = cls.query().fetch()
      cls._CATEGORY_INFO = [(c.key.id(), c.key.id()) for c in cats
                            if c.key.id() != cls._ROOT]
    return cls._CATEGORY_INFO


class Video(ndb.Model):
  """Model for Video data. A Video entity will be built for each video,
  and have an associated search.Document. The Video entity does not include
  all of the fields in its corresponding indexed product document, only 'core'
  fields."""

  doc_id = ndb.StringProperty()  # the id of the associated document
  duration_min = ndb.IntegerProperty(default=0)
  category = ndb.StringProperty()
  # average rating of the video over all its reviews
  avg_rating = ndb.FloatProperty(default=0)
  # the number of reviews of that product
  num_reviews = ndb.IntegerProperty(default=0)
  active = ndb.BooleanProperty(default=True)
  # indicates whether the associated document needs to be re-indexed due to a
  # change in the average review rating.
  needs_review_reindex = ndb.BooleanProperty(default=False)

  @property
  def vid(self):
    return self.key.id()

  def reviews(self):
    """Retrieve all the (active) associated reviews for this product, via the
    reviews' video_key field."""
    return Review.query(Review.active == True, Review.rating_added == True,
                        Review.video_key == self.key).fetch()

  @classmethod
  def updateVideoDocsWithNewRating(cls, pkeys):
    """Given a list of Video entity keys, check each entity to see if it is
    marked as needing a document re-index.  This flag is set when a new review
    is created for that video, and config.BATCH_RATINGS_UPDATE = True.
    Generate the modified docs as needed and batch re-index them."""

    doclist = []

    def _tx(vid):
      v = cls.get_by_id(vid)
      if v and v.needs_review_reindex:

        # update the associated document with the new ratings info
        # and reindex
        modified_doc = docs.Video.updateRatingInDoc(v.doc_id, v.avg_rating)
        if modified_doc:
          doclist.append(modified_doc)
        v.needs_review_reindex = False
        v.put()

    for pkey in pkeys:
      ndb.transaction(lambda: _tx(pkey.id()))
    # reindex all modified docs in batch
    docs.Video.add(doclist)

  @classmethod
  def create(cls, params, doc_id):
    """Create a new Video entity from a subset of the given params dict
    values, and the given doc_id."""
    v = cls(
        id=params['vid'],
        duration_min=int(params['duration_min']),
        category=params['category'],
        doc_id=doc_id)
    v.put()
    return v

  def update_core(self, params, doc_id):
    """Update 'core' values from the given params dict and doc_id."""
    self.populate(
        duration_min=int(params['duration_min']),
        category=params['category'],
        doc_id=doc_id)

  @classmethod
  def updateVideoDocWithNewRating(cls, vid):
    """Given the id of a Video entity, see if it is marked as needing
    a document re-index.  This flag is set when a new review is created for
    that video.  If it needs a re-index, call the document method."""

    def _tx():
      v = cls.get_by_id(vid)
      if v and v.needs_review_reindex:
        v.needs_review_reindex = False
        v.put()
      return (v.doc_id, v.avg_rating)

    (doc_id, avg_rating) = ndb.transaction(_tx)
    # update the associated document with the new ratings info
    # and reindex
    docs.Video.updateRatingsInfo(doc_id, avg_rating)


class Review(ndb.Model):
  """Model for Review data. Associated with a Video entity via the video
  key."""

  doc_id = ndb.StringProperty()
  date_added = ndb.DateTimeProperty(auto_now_add=True)
  video_key = ndb.KeyProperty(kind=Video)
  username = ndb.StringProperty()
  rating = ndb.IntegerProperty()
  active = ndb.BooleanProperty(default=True)
  comment = ndb.TextProperty()
  rating_added = ndb.BooleanProperty(default=False)

  @classmethod
  def deleteReviews(cls, vid):
    """Deletes the reviews associated with a Video id."""
    if not vid:
      return
    reviews = cls.query(cls.video_key == ndb.Key(Video, vid)).fetch(
        keys_only=True)
    return ndb.delete_multi(reviews)
