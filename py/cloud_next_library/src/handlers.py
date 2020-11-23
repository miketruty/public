# Copyright 2018 Google Inc. All Rights Reserved.
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
"""Contains the non-admin ('user-facing') request handlers for the app."""

import datetime
import logging
import urllib
import wsgiref

from base_handler import BaseHandler
import categories
import config
import docs
import models  # For reviews mostly.
# TODO: test running this WITHOUT IAP to ensure folks can use without
#       being logged in - if we ever release outside of Google.
from oauth_utils import decorator
import playlists
import search_queries
import utils
import youtube_service

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb
import google.appengine.ext.deferred as deferred


def SetupTemplateValues():
  """Commonly used initialization of template values."""
  return {
      'cat_info': models.Category.getCategoryInfo(),
      'sort_info': docs.Video.getSortMenu(),
  }


def StripCommas(input_s):
  """Strip empty commas."""
  if not input_s:
    return ''
  return ', '.join(
      filter(None, (s.strip() for s in input_s.split(','))))


class IndexHandler(BaseHandler):
  """Displays the 'home' page."""

  @decorator.oauth_aware
  def get(self):
    self.render_template('index.html', SetupTemplateValues())


class PlaylistsHandler(BaseHandler):
  """Displays the 'Playlists' page."""

  @decorator.oauth_aware
  def get(self):
    t = SetupTemplateValues()
    t['playlists18'] = playlists.NEXT18_PLAYLISTS
    self.render_template('playlists.html', t)


class InternalLinksHandler(BaseHandler):
  """Displays the Internal Links page."""

  @decorator.oauth_aware
  def get(self):
    self.render_template('internal_links.html', SetupTemplateValues())


class OfficialNext18Handler(BaseHandler):
  """Displays the Official Next '18 searches page."""

  @decorator.oauth_aware
  def get(self):
    self.render_template('officialnext18.html', SetupTemplateValues())


class OfficialNext19Handler(BaseHandler):
  """Displays the Official Next '19 searches page."""

  @decorator.oauth_aware
  def get(self):
    self.render_template('officialnext19.html', SetupTemplateValues())


class ShowRecommendationsHandler(BaseHandler):
  """Display Session Recommendations details."""

  @decorator.oauth_aware
  def get(self):
    """Do document search for unique id and display the retrieved fields."""
    self.render_template('recommendations_searches.html', SetupTemplateValues())


class SearchHintsHandler(BaseHandler):
  """Displays the 'Search Hints' page."""

  @decorator.oauth_aware
  def get(self):
    self.render_template('criteria_hints.html', SetupTemplateValues())


class LearningSearchesHandler(BaseHandler):
  """Displays learning searches examples page."""

  @decorator.oauth_aware
  def get(self):
    t = SetupTemplateValues()
    t['searches'] = self.encodeSearches(search_queries.LEARNING_SEARCHES)
    self.render_template('learning_searches.html', t)


class VideoSearchesHandler(BaseHandler):
  """Displays video searches examples page."""

  @decorator.oauth_aware
  def get(self):
    t = SetupTemplateValues()
    t['searches'] = self.encodeSearches(search_queries.VIDEO_SEARCHES)
    self.render_template('video_searches.html', t)


class SolutionSearchesHandler(BaseHandler):
  """Displays solution searches examples page."""

  @decorator.oauth_aware
  def get(self):
    t = SetupTemplateValues()
    t['searches'] = self.encodeSearches(search_queries.SOLUTION_SEARCHES)
    self.render_template('solution_searches.html', t)


class ShowDetailsHandler(BaseHandler):
  """Display video details."""

  def parseParams(self):
    """Filter the param set to the expected params."""
    # The dict can be modified to add any defined defaults.
    params = {
        'uniqueid': '',
        'vid': '',
        'title': '',
        'comment': '',
        'rating': '',
        'category': '',
        'recommendations': '',
    }
    for k, v in params.iteritems():
      # Possibly replace default values.
      params[k] = self.request.get(k, v)
    return params

  def getTemplateValues(self):
    """Do document search for the unique id and display the retrieved fields."""
    params = self.parseParams()

    uniqueid = params['uniqueid']
    if not uniqueid:
      # we should not reach this
      msg = 'Error: do not have unique id.'
      url = '/'
      linktext = 'Go to video search page.'
      self.render_template('notification.html', {
          'title': 'Error',
          'msg': msg,
          'goto_url': url,
          'linktext': linktext
      })
      return
    doc = docs.Video.getDocFromUid(uniqueid)
    if not doc:
      error_message = ('Document not found for uniqueid %s.' % uniqueid)
      logging.error(error_message)
      return self.abort(404, error_message)
    vdoc = docs.Video(doc)
    title = vdoc.getTitle()
    # app_url = wsgiref.util.application_uri(self.request.environ)
    # rlink = '/reviews?' + urllib.urlencode({'uniqueid': uniqueid, 'title': title})
    rlink = ''
    template_values = {
        # 'app_url':
        #     app_url,
        'uniqueid':
            uniqueid,
        'vid':
            vdoc.getVID(),
        'title':
            title,
        # 'review_link':
        #     rlink,
        # 'comment':
        #     params['comment'],
        # 'rating':
        #     params['rating'],
        'category':
            vdoc.getCategory(),
        'subtitle':
            vdoc.getSubtitle(),
        'image':
            vdoc.getImage(),
        'prod_doc':
            doc,
        'user_is_loggedin':
            users.get_current_user(),
        'user_is_googler':
            users.get_current_user().email().endswith('@google.com'),
    }
    return template_values


class ShowLearningDetailsHandler(ShowDetailsHandler):
  """Display learning details."""

  @decorator.oauth_aware
  def get(self):
    """Do document search for the unique id and display the retrieved fields."""
    self.render_template('learningdetails.html', self.getTemplateValues())


class ShowVideoHandler(ShowDetailsHandler):
  """Display video details."""

  @decorator.oauth_aware
  def get(self):
    """Do document search for the unique id and display the retrieved fields."""
    self.render_template('video.html', self.getTemplateValues())


class ShowAccelerateHandler(ShowDetailsHandler):
  """Display Accelerate details."""

  @decorator.oauth_aware
  def get(self):
    """Do document search for unique id and display the retrieved fields."""
    self.render_template('accelerate.html', self.getTemplateValues())


class ShowSolutionHandler(ShowDetailsHandler):
  """Display Solution details."""

  @decorator.oauth_aware
  def get(self):
    """Do document search for unique id and display the retrieved fields."""
    self.render_template('solution.html', self.getTemplateValues())


class CreateReviewHandler(BaseHandler):
  """Process the submission of a new review."""

  def parseParams(self):
    """Filter the param set to the expected params."""
    params = {
        'vid': '',
        'title': '',
        'comment': 'this is a great video',
        'rating': '5',
        'category': ''
    }
    for k, v in params.iteritems():
      # Possibly replace default values.
      params[k] = self.request.get(k, v)
    return params

  @decorator.oauth_required
  def post(self):
    """Create a new review entity from the submitted information."""
    self.createReview(self.parseParams())

  def createReview(self, params):
    """Create a new review entity from the information in the params dict."""
    author = users.get_current_user()
    comment = params['comment']
    vid = params['vid']
    title = params['title']
    if not vid:
      msg = 'Could not get vid; aborting creation of review.'
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
    if not comment:
      logging.info('comment not provided')
      self.redirect('/video?' + urllib.urlencode(params))
      return
    rstring = params['rating']
    # confirm that the rating is an int in the allowed range.
    try:
      rating = int(rstring)
      if rating < config.RATING_MIN or rating > config.RATING_MAX:
        logging.warn('Rating %s out of allowed range', rating)
        params['rating'] = ''
        self.redirect('/video?' + urllib.urlencode(params))
        return
    except ValueError:
      logging.error('bad rating: %s', rstring)
      params['rating'] = ''
      self.redirect('/video?' + urllib.urlencode(params))
      return
    review = self.createAndAddReview(vid, author, rating, comment)
    video_url = '/video?' + urllib.urlencode({'vid': vid, 'title': title})
    if not review:
      msg = 'Error creating review.'
      logging.error(msg)
      self.render_template('notification.html', {
          'title': 'Error',
          'msg': msg,
          'goto_url': video_url,
          'linktext': 'Back to video.'
      })
      return
    rparams = {'video_url': video_url, 'title': title, 'review': review}
    self.render_template('review.html', rparams)

  def createAndAddReview(self, vid, user, rating, comment):
    """Given review information, create the new review entity.

    Point via key to the associated 'parent' video entity.
    Get the account info of the user submitting the review. If the
    client is not logged in (which is okay), just make them 'anonymous'.

    Args:
      vid: Video ID of video to review.
      user: User creating the review.
      rating: Review rating.
      comment: String comment explaining the review rationale.

    Returns:
      The created review.
    """
    if user:
      username = user.nickname().split('@')[0]
    else:
      username = 'anonymous'

    prod = models.Video.get_by_id(vid)
    if not prod:
      error_message = 'could not get video for vid %s' % vid
      logging.error(error_message)
      return self.abort(404, error_message)

    rid = models.Review.allocate_ids(size=1)[0]
    key = ndb.Key(models.Review._get_kind(), rid)

    def _tx():
      review = models.Review(
          key=key,
          video_key=prod.key,
          username=username,
          rating=rating,
          comment=comment)
      review.put()
      # in a transactional task, update the parent video's average
      # rating to include this review's rating, and flag the review as
      # processed.
      deferred.defer(utils.updateAverageRating, key, _transactional=True)
      return review

    return ndb.transaction(_tx)


class VideoSearchHandler(BaseHandler):
  """The handler for doing a video search."""

  _OFFSET_LIMIT = 1000

  def parseParams(self):
    """Filter the param set to the expected params."""
    params = {
        'qtype': '',
        'category': '',
        'sort': '',
        'rating': '',
        'offset': '0',
        'create_playlist': '',
        'recommendations': '',
    }
    for k, v in params.iteritems():
      # Possibly replace default values.
      params[k] = self.request.get(k, v)

    # Default query but only when the page is initially loaded, not when
    # query is purposely set to ''.
    params['query'] = (config.DEFAULT_QUERY
                       if 'query' not in self.request.arguments() else
                       self.request.get('query'))
    # For MDL UI 'Any Event' must have a value. But the search must
    # have nothing in that case. So, just strip it for the search.
    if params['category'] == 'anyevent':
      params['category'] = ''
    return params

  @decorator.oauth_aware
  def post(self):
    params = self.parseParams()
    self.redirect('/vsearch?' + urllib.urlencode(
        dict([k, v.encode('utf-8')] for k, v in params.items())))

  def _getDocLimit(self, create_playlist=False):
    return int(self._OFFSET_LIMIT if create_playlist else config.DOC_LIMIT)

  @decorator.oauth_aware
  def get(self):
    """Handle a video search request."""
    params = self.parseParams()
    self.doVideoSearch(params)

  @decorator.oauth_required
  def _createPlaylist(self, vids):
    """Create YouTube playlist from the list of video ids."""
    pid = None
    playlist_name = None
    if vids:
      timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
      playlist_name = '%s Search Results Playlist' % timestamp
      description = 'Created by %s.' % users.get_current_user()
      pid = youtube_service.CreatePlaylist(
          credentials=decorator.credentials,
          playlist_name=playlist_name,
          description=description)
      if pid:
        youtube_service.AddPlaylistItems(decorator.credentials, pid, vids)

    self.render_template('create_playlist.html', {
        'pid': pid,
        'vid_count': len(vids),
        'playlist_name': playlist_name
    })

  def doVideoSearch(self, params):
    """Perform a video search and display the results."""
    # If NOT creating a playlist, get a page of full results.
    # If creating a playlist, do the search for all items but return
    # only video_ids.
    create_playlist = params.get('create_playlist')
    show_recommendations = (params.get('recommendations', '') == 'yes')

    sort_dict = docs.Video.getSortDict()
    query = params.get('query', '')
    user_query = query
    doc_limit = self._getDocLimit(create_playlist or show_recommendations)

    categoryq = params.get('category')
    if categoryq:
      # add specification of the category to the query
      # Because the category field is atomic, put the category string
      # in quotes for the search.
      query += ' %s:"%s"' % (docs.Video.CATEGORY, categoryq)

    sortq = params.get('sort') if params.get('sort') else config.DEFAULT_SORTQ

    offsetval = 0
    if (not create_playlist) and ('offset' in params):
      offsetval = int(params.get('offset', 0))

    # Check to see if the query parameters include a ratings filter, and
    # add that to the final query string if so.  At the same time, generate
    # 'ratings bucket' counts and links-- based on the query prior to addition
    # of the ratings filter-- for sidebar display.
    query, rlinks = self._generateRatingsInfo(params, query, user_query, sortq,
                                              categoryq)
    logging.debug('query: %s', query.strip())

    try:
      # build the query and perform the search
      search_query = self._buildQuery(
          query=query,
          sortq=sortq,
          sort_dict=sort_dict,
          doc_limit=doc_limit,
          offsetval=offsetval,
          create_playlist=create_playlist,
          show_recommendations=show_recommendations)
      search_results = docs.Video.getIndex().search(search_query)
      returned_count = len(search_results.results)
      logging.info('Returned: %s.', returned_count)

    except search.Error:
      logging.exception('Search error:')  # log the exception stack trace
      msg = 'There was a search error (see logs).'
      url = '/'
      linktext = 'Go to video search page.'
      self.render_template('notification.html', {
          'title': 'Error',
          'msg': msg,
          'goto_url': url,
          'linktext': linktext
      })
      return

    if create_playlist:
      vids = []
      for doc in search_results:
        d = docs.Video(doc)
        if d.getCategory() not in categories.YOUTUBE_CATS:
          continue
        vid = d.getVID()
        if vid:
          vids.append(vid)

      if vids:
        self._createPlaylist(vids=vids)

      return

    # cat_name = models.Category.getCategoryName(categoryq)
    search_response = []
    # For each document returned from the search
    for doc in search_results:
      # logging.info("doc: %s ", doc)
      vdoc = docs.Video(doc)

      # get field information from the returned doc
      uniqueid = vdoc.getUniqueID()
      vid = vdoc.getVID()
      cat = vdoc.getCategory()
      title = vdoc.getTitle()
      # use the description field as the default description snippet, since
      # snippeting is not supported on the dev app server.
      # Remove trailing empty commas, and embedded empty commas.
      subtitle = StripCommas(vdoc.getSubtitle())
      description_snippet = vdoc.getDescription()
      # on the dev app server, the doc.expressions property won't be populated.
      for expr in doc.expressions:
        if expr.name == docs.Video.DESCRIPTION:
          description_snippet = expr.value
      # Remove trailing empty commas, and embedded empty commas.
      speakers = StripCommas(vdoc.getSpeakers())
      duration_min = vdoc.getDurationMin()
      published_date = vdoc.getPublishedDate()
      # uncomment to use 'adjusted duration_min', which should be
      # defined in returned_expressions in _buildQuery() below, as the
      # displayed duration_min.
      # elif expr.name == 'adjusted_duration_min':
      # duration_min = expr.value
      views = vdoc.getViews()
      slides_link = vdoc.getSlidesLink()
      tags = vdoc.getTags()
      image = vdoc.getImage()
      sessionid = vdoc.getSessionID()
      avg_rating = vdoc.getAvgRating()
      # for this result, generate a result array of selected doc fields, to
      # pass to the template renderer
      search_response.append({
          'doc': doc,
          'uniqueid': uniqueid,
          'vid': urllib.quote_plus(vid),
          'cat': cat,
          'desc': description_snippet,
          'duration': duration_min,
          'published_date': published_date,
          'slides_link': slides_link,
          'speakers': speakers,
          'subtitle': subtitle,
          'title': title,
          'views': views,
          'tags': tags,
          'image': image,
          'sessionid': sessionid,
          'avg_rating': avg_rating
      })
    if not query:
      print_query = 'All'
    else:
      print_query = query

    # Build the next/previous pagination links for the result set.
    (prev_link, next_link) = self._generatePaginationLinks(
        offsetval, returned_count, search_results.number_found, params)

    logging.debug('returned_count: %s', returned_count)
    # construct the template values
    template_values = SetupTemplateValues()
    template_values.update({
        'base_pquery':
            user_query,
        'next_link':
            next_link,
        'prev_link':
            prev_link,
        'qtype':
            'video',
        'query':
            query,
        'recommendations':
            params.get('recommendations', ''),
        'print_query':
            print_query,
        'sort_order':
            sortq,
        'category_name':
            categoryq,
        'first_res':
            offsetval + 1,
        'last_res':
            offsetval + returned_count,
        'returned_count':
            returned_count,
        'number_found':
            # There's a bug here. When searching with empty query, this
            # is sometimes returning a crazy number. Adjust the UI.
            # 1000 is the AppEngine doc result max offset allowed.
            utils.intClamp(search_results.number_found, 0, 1000),
        'search_response':
            search_response,
        'ratings_links':
            rlinks,
        'current_user':
            users.get_current_user(),
        'user_is_googler':
            users.get_current_user().email().endswith('@google.com'),
    })
    # Handle a simpler recommendations output page.
    if show_recommendations:
      self.render_template('recommendations.html', template_values)
    else:
      # Render the result page.
      self.render_template('index.html', template_values)

  def _buildQuery(self, query, sortq, sort_dict, doc_limit, offsetval,
                  create_playlist, show_recommendations):
    """Build and return a search query object."""
    # computed and returned fields examples.  Their use is not required
    # for the application to function correctly.
    # computed_expr = search.FieldExpression(
    #     name='adjusted_duration_min', expression='duration_min * 1.08')
    returned_fields = ([
        docs.Video.UNIQUEID,
        docs.Video.TITLE,
        docs.Video.CATEGORY,
        docs.Video.SUBTITLE,
        docs.Video.DURATION_MIN,
        docs.Video.SPEAKERS,
        docs.Video.DESCRIPTION,
        docs.Video.PUBLISHED_DATE,
        docs.Video.VIEWS,
        docs.Video.SLIDES_LINK,
        docs.Video.TAGS,
        docs.Video.IMAGE,
        docs.Video.VID,
        docs.Video.SESSIONID,
        docs.Video.AVG_RATING,
    ] if not create_playlist else [docs.Video.VID, docs.Video.CATEGORY])

    if sortq == 'relevance':
      # If sorting on 'relevance', use the Match scorer which is based on
      # sort options.
      sortopts = search.SortOptions(match_scorer=search.MatchScorer())
      search_query = search.Query(
          query_string=query.strip(),
          options=search.QueryOptions(
              limit=doc_limit,
              offset=offsetval,
              sort_options=sortopts,
              snippeted_fields=(
                  [] if show_recommendations else [docs.Video.DESCRIPTION]),
              # returned_expressions=[computed_expr],
              returned_fields=returned_fields))
    else:
      # Otherwise (not sorting on relevance), use the selected field as the
      # first dimension of the sort expression, and the average rating as the
      # second dimension, unless we're sorting on rating, in which case
      # duration_min is the second sort dimension.
      # We get the sort direction and default from the 'sort_dict' var.
      if sortq == docs.Video.AVG_RATING:
        expr_list = [
            sort_dict.get(sortq), sort_dict.get(docs.Video.DURATION_MIN)
        ]
      else:
        # expr_list = [sort_dict.get(sortq),
        #              sort_dict.get(docs.Video.AVG_RATING)]
        expr_list = [sort_dict.get(sortq)]
      sortopts = search.SortOptions(expressions=expr_list)
      # logging.info("sortopts: %s", sortopts)
      search_query = search.Query(
          query_string=query.strip(),
          options=search.QueryOptions(
              limit=doc_limit,
              offset=offsetval,
              sort_options=sortopts,
              snippeted_fields=(
                  [] if show_recommendations else [docs.Video.DESCRIPTION]),
              # returned_expressions=[computed_expr],
              returned_fields=returned_fields))
    return search_query

  def _generateRatingsInfo(self, params, query, user_query, sort, category):
    """Add ratings filter to query and build sidebar ratings content."""
    orig_query = query
    try:
      n = int(params.get('rating', 0))
      # check that rating is not out of range
      if n < config.RATING_MIN or n > config.RATING_MAX:
        n = None
    except ValueError:
      n = None
    if n:
      if n < config.RATING_MAX:
        query += ' %s >= %s %s < %s' % (docs.Video.AVG_RATING, n,
                                        docs.Video.AVG_RATING, n + 1)
      else:  # max rating
        query += ' %s:%s' % (docs.Video.AVG_RATING, n)
    query_info = {
        'query': user_query.encode('utf-8'),
        'sort': sort,
        'category': category
    }
    rlinks = docs.Video.generateRatingsLinks(orig_query, query_info)
    return (query, rlinks)

  def _generatePaginationLinks(self, offsetval, returned_count, number_found,
                               params):
    """Generate the next/prev pagination links for the query.

    Detect when we're out of results in a given direction and don't generate
    the link in that case.
    """
    doc_limit = self._getDocLimit()
    pcopy = params.copy()
    if offsetval - doc_limit >= 0:
      pcopy['offset'] = offsetval - doc_limit
      prev_link = '/vsearch?' + urllib.urlencode(pcopy)
    else:
      prev_link = None
    if ((offsetval + doc_limit <= self._OFFSET_LIMIT) and
        (returned_count == doc_limit) and
        (offsetval + returned_count < number_found)):
      pcopy['offset'] = offsetval + doc_limit
      next_link = '/vsearch?' + urllib.urlencode(pcopy)
    else:
      next_link = None
    return (prev_link, next_link)


class ShowReviewsHandler(BaseHandler):
  """Show the reviews for a given video.

  This information is pulled from the datastore Review entities.
  """

  @decorator.oauth_required
  def get(self):
    """Show list of reviews for video indicated by 'vid' request parameter."""
    vid = self.request.get('vid')
    title = self.request.get('title')
    if vid:
      # find the video entity corresponding to that vid
      prod = models.Video.get_by_id(vid)
      if prod:
        # get the video's average rating, over all its reviews
        # get the list of review entities for the video
        avg_rating = prod.avg_rating
        reviews = prod.reviews()
        logging.debug('reviews: %s', reviews)
      else:
        error_message = 'could not get video for vid %s' % vid
        logging.error(error_message)
        return self.abort(404, error_message)
      rlist = [[r.username, r.rating, str(r.comment)] for r in reviews]

      # build a template dict with the review and video information
      video_url = '/video?' + urllib.urlencode({'vid': vid, 'title': title})
      template_values = {
          'rlist': rlist,
          'video_url': video_url,
          'title': title,
          'avg_rating': avg_rating
      }
      # render the template.
      self.render_template('reviews.html', template_values)
