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
""" Holds configuration settings.
"""

VIDEO_INDEX_NAME = 'videosearch1'  # The document index name.
# An index name must be a visible printable
# ASCII string not starting with '!'. Whitespace characters are
# excluded.

DEFAULT_QUERY = 'next2020'  # Initially load page with something.
DEFAULT_SORTQ = 'views'  # Or title.

# From YouTube metadata
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
FIELD_SUBTITLE = 'subtitle'
FIELD_TAGS = 'tags'
FIELD_IMAGE = 'image'

FIELD_YOUTUBE = 'youtube'  # Used as a suffix.

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

# set BATCH_RATINGS_UPDATE to False to update documents with changed ratings
# info right away.  If True, updates will only occur when triggered by
# an admin request or a cron job.  See cron.yaml for an example.
BATCH_RATINGS_UPDATE = False
# BATCH_RATINGS_UPDATE = True

# The max and min (integer) ratings values allowed.
RATING_MIN = 1
RATING_MAX = 5

# The number of search results to display per page
DOC_LIMIT = 10

VIDEO_DATA = 'video_data.csv'

# TODO: adjust update case.
DEMO_UPDATE_BOOKS_DATA = 'sample_data_books_update.csv'

# the size of the import batches, when reading from the csv file.  Must not
# exceed 100.
IMPORT_BATCH_SIZE = 20

# For pubsub notification.
PUBSUB_TOPIC = 'projects/gcp-next-reviewdeo/topics/metadata-file-updated'
PUBSUB_VERIFICATION_TOKEN = 'xx'
