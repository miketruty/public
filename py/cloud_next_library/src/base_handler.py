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
""" The base request handler class.
"""

import webapp2
from webapp2_extras import jinja2
import json
import urllib

from google.appengine.api import users

import search_queries


_FEEDBACK_URL = 'https://groups.google.com/a/google.com/forum/#!forum/cloud-next-library-feedback'


def toJSSafeArg(arg_string):
  """Remove unsafe characters from JavaScript argument string."""
  replacements = ['\'', '?', ';']
  for r in replacements:
    arg_string = arg_string.replace(r, '')
  return arg_string


class BaseHandler(webapp2.RequestHandler):
  """The other handlers inherit from this class.  Provides some helper methods
  for rendering a template and generating template links."""

  @classmethod
  def logged_in(cls, handler_method):
    """This decorator requires a logged-in user, and returns 403 otherwise.
    """

    def auth_required(self, *args, **kwargs):
      if (users.get_current_user() or
          self.request.headers.get('X-AppEngine-Cron')):
        handler_method(self, *args, **kwargs)
      else:
        self.error(403)

    return auth_required

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render_template(self, filename, template_args):
    template_args.update(self.generateSidebarLinksDict())
    env = self.jinja2
    env.environment.filters['tojssafearg'] = toJSSafeArg
    #print '---------------------------------------------------'
    #print env.environment.filters
    #print '---------------------------------------------------'
    # self.response.write(self.jinja2.render_template(filename, **template_args))
    self.response.write(env.render_template(filename, **template_args))

  def render_json(self, response):
    self.response.write('%s(%s);' % (self.request.GET['callback'],
                                     json.dumps(response)))

  def getLoginLink(self):
    """Generate login or logout link and text, depending upon the logged-in
    status of the client."""
    current_user = users.get_current_user()
    if current_user:
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout from: %s' % current_user
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'
    return (url, url_linktext)

  def getAdminManageLink(self):
    """Build link to the admin management page, if the user is app admin."""
    if users.is_current_user_admin():
      admin_url = '/admin/manage'
      return (admin_url, 'Admin tasks')
    else:
      return (None, None)

  def createProductAdminLink(self):
    if users.is_current_user_admin():
      admin_create_url = '/admin/create_product'
      return (admin_create_url, 'Create new product (admin)')
    else:
      return (None, None)

  def encodeSearches(self, searches):
    """Helper to properly build search links."""
    search_list = []
    for s in searches:
      d = search_queries.DEFAULT_SEARCH.copy()
      label = s.copy().pop('label', s.get('query', ''))
      d.update(s)
      search_list.append(
          ('&'.join(['%s=%s' % (k, urllib.quote(v))
                     for k, v in d.iteritems()]),
           label))
    return search_list

  def generateSidebarLinksDict(self):
    """Build a dict containing login/logout and admin links, which will be
    included in the sidebar for all app pages."""

    loginlogout_url, url_linktext = self.getLoginLink()
    admin_create_url, admin_create_text = self.createProductAdminLink()
    admin_url, admin_text = self.getAdminManageLink()
    return {
        'admin_create_url': admin_create_url,
        'admin_create_text': admin_create_text,
        'admin_url': admin_url,
        'admin_text': admin_text,
        'feedback_url': _FEEDBACK_URL,
        'next18_other': self.encodeSearches(
            search_queries.NEXT18_SESSION_OTHER),
        'next18_themes': self.encodeSearches(
            search_queries.NEXT18_SESSION_THEMES),
        'next18_types': self.encodeSearches(
            search_queries.NEXT18_SESSION_TYPES),
        'next19_types': self.encodeSearches(
            search_queries.NEXT19_SESSION_TYPES),
        'next19_levels': self.encodeSearches(
            search_queries.NEXT19_LEARNING_LEVELS),
        'next19_tracks': self.encodeSearches(
            search_queries.NEXT19_SESSION_TRACKS),
        'next19_industries': self.encodeSearches(
            search_queries.NEXT19_SESSION_INDUSTRIES),
        'url': loginlogout_url,
        'url_linktext': url_linktext
    }
