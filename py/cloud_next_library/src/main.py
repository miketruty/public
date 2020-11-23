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
"""Defines the routing for the app's non-admin handlers.
"""

from handlers import *
import webapp2

from oauth_utils import decorator

application = webapp2.WSGIApplication(
    [
        ('/', VideoSearchHandler),
        ('/accelerate', ShowAccelerateHandler),
        ('/internallinks', InternalLinksHandler),
        ('/learningdetails', ShowLearningDetailsHandler),
        ('/officialnext18', OfficialNext18Handler),
        ('/officialnext19', OfficialNext19Handler),
        ('/playlists', PlaylistsHandler),
        ('/search_hints', SearchHintsHandler),
        ('/recommendations', ShowRecommendationsHandler),
        ('/solution', ShowSolutionHandler),
        ('/solutionsearches', SolutionSearchesHandler),
        ('/video', ShowVideoHandler),
        ('/learningsearches', LearningSearchesHandler),
        ('/videosearches', VideoSearchesHandler),
        ('/vsearch', VideoSearchHandler),
        # ('/reviews', ShowReviewsHandler),
        # ('/create_review', CreateReviewHandler),
        (decorator.callback_path, decorator.callback_handler()),
    ],
    debug=True)
