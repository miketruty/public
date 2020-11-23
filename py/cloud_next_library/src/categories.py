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
"""Specifies product category information for the app.
"""
from google.appengine.api import search

# NOTE: The categories are *cached* in the datastore. If you add/remove a
#       category, you *must* remove all the categories in the data store to
#       *see* your updates.

CAT_NEXT2016 = 'next2016'
CAT_NEXT2017 = 'next2017'
CAT_NEXT2018 = 'next2018'
CAT_NEXT2019 = 'next2019'
CAT_NEXT2020 = 'next2020'
CAT_ACCELERATE2017 = 'accelerate2017'
CAT_SOLUTION = 'solution'
CAT_LEARNING = 'learning'

ALL_CATS = [
    CAT_NEXT2016,
    CAT_NEXT2017,
    CAT_NEXT2018,
    CAT_NEXT2019,
    CAT_NEXT2020,
    CAT_ACCELERATE2017,
    CAT_SOLUTION,
    CAT_LEARNING,
]

YOUTUBE_CATS = [
    CAT_NEXT2016,
    CAT_NEXT2017,
    CAT_NEXT2018,
    CAT_NEXT2019,
    CAT_NEXT2020,
]

cats = [{'name': c, 'children': []}
        for c in ALL_CATS]

ctree = {'name': 'root', 'children': cats}

# [The core fields that all videos share are:
#  title,
#  category,
#  subtitle,
#  duration_min,
#  speakers,
#  description,
#  image,
#  published_date,
#  tags,
#  views,
# ]

# Define the non-'core' (differing) product fields for each category
# above, and their types.
event_dict = {c: {} for c in ALL_CATS}
