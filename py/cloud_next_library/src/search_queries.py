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
""" For our favorite search queries.
"""

import config

# Default:
# {category, sort=title,
DEFAULT_SEARCH = {
    'category': '',
    'sort': config.DEFAULT_SORTQ,
    'rating': '',
    'create_playlist': '',
    'offset': 0,
    'qtype': 'event',
    'recommendations': '',
}

LEARNING_SEARCHES = [
    {
        'label': 'All Learning Courses',
        'category': 'learning',
        'query': 'qlCourse',
        'sort': 'title',
    },
    {
        'label': 'All Learning Modules',
        'category': 'learning',
        'query': 'qlModule',
        'sort': 'title',
    },
    {
        'label': 'All Learning Quests',
        'category': 'learning',
        'query': 'qlQuest',
        'sort': 'title',
    },
    {
        'label': 'All Learning Labs',
        'category': 'learning',
        'query': 'qlLab',
        'sort': 'title',
    },
    {
        'label': 'Learning SPLs',
        'category': 'learning',
        'query': 'qlLab AND SPL',
        'sort': 'title',
    },
    {
        'label': 'Learning non-SPL Labs',
        'category': 'learning',
        'query': 'qlLab AND NOT SPL',
        'sort': 'title',
    },
]

VIDEO_SEARCHES = [
    {
        'label': 'All (most popular)',
        'query': '',
        'sort': 'views',  # Most popular, based on views.
    },
    {
        'label': 'All Next \'19 sessions',
        'category': 'next2019',
        'query': '',
        'sort': 'views',  # Most popular, based on views.
    },
    {
        'label': 'All Next \'18 videos',
        'category': 'next2018',
        'query': '',
        'sort': 'views',  # Most popular, based on views.
    },
    {
        'label': 'Next \'18 keynotes',
        'query': 'title:keynote',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'query': 'big data',
    },
    {
        'query': 'collaboration OR productivity',
    },
    {
        'query': 'container OR kubernetes',
    },
    {
        'query': 'duration_min < 30',
    },
    {
        'query': 'title:keynote event:next2018',
    },
    {
        'query': 'title:keynote event:next2017',
    },
    {
        'query': 'title:keynote event:next2016',
    },
    {
        'query': 'machine learning',
    },
    {
        'query': 'migrate OR migration',
    },
    {
        'query': 'mobile OR mobility',
    },
    {
        'query': 'partner OR partnering',
    },
    {
        'query': 'security',
    },
    {
        'query': 'speakers:urs OR speakers:treynor OR speakers:kava',
    },
    {
        'query': 'speakers:"developer relations"',
    },
    {
        'query': 'speakers:"solutions architect"',
    },
    {
        'query': 'subtitle:"application development"',
    },
    {
        'query': 'subtitle:"big data & machine learning"',
    },
    {
        'query': 'subtitle:"collaboration & productivity"',
    },
    {
        'query': 'subtitle:"connected business platform"',
    },
    {
        'query': 'subtitle:"infrastructure & operations"',
    },
    {
        'query': 'subtitle:"mobility & devices"',
    },
    {
        'label': 'Accelerate Keynotes',
        'query': 'title:keynote',
        'category': 'accelerate2017',
        'sort': 'title',
    },
]

SOLUTION_SEARCHES = [
    {
        'label': 'All Solutions',
        'query': '',
        'category': 'solution',
        'sort': 'title',
    },
    {
        'label': 'Machine Learning Solutions',
        'query': 'machine learning',
        'category': 'solution',
    },
    {
        'label': 'Migration Solutions',
        'query': 'migrate OR migration',
        'category': 'solution',
    },
    {
        'label': 'Mobile Solutions',
        'query': 'mobile OR mobility',
        'category': 'solution',
    },
    {
        'label': 'Security Solutions',
        'query': 'security',
        'category': 'solution',
    },
]

NEXT18_SESSION_THEMES = [
    {
        'label': 'Application Development',
        'query': 'subtitle:"Application Development"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Collaboration & Productivity',
        'query': 'subtitle:"Collaboration & Productivity"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Data Analytics',
        'query': 'subtitle:"Data Analytics"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'IoT',
        'query': 'subtitle:"IoT"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Infrastructure & Operations',
        'query': 'subtitle:"Infrastructure & Operations"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Machine Learning & AI',
        'query': 'subtitle:"Machine Learning & AI"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Mobility & Devices',
        'query': 'subtitle:"Mobility & Devices"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Security',
        'query': 'subtitle:"Security"',
        'category': 'next2018',
        'sort': 'views',
    },
]

NEXT18_SESSION_OTHER = [
    {
        'label': 'Compute',
        'query': 'compute',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Database and Storage',
        'query': 'database OR storage',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Healthcare',
        'query': 'healthcare',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Hybrid',
        'query': 'hybrid',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Networking',
        'query': 'network OR networking',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Serverless',
        'query': 'serverless',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Tensorflow - TPU',
        'query': 'tensorflow OR TPU',
        'category': 'next2018',
        'sort': 'views',
    },
]

NEXT18_SESSION_TYPES = [
    {
        'label': 'Breakout',
        'query': 'subtitle:"Breakout"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Panel',
        'query': 'subtitle:"Panel"',
        'category': 'next2018',
        'sort': 'views',
    },
    {
        'label': 'Bootcamps',
        'query': 'subtitle:"Bootcamps"',
        'category': 'next2018',
        'sort': 'title',
    },
]

NEXT19_SESSION_TYPES = [
    {
        'label': 'Breakout (347)',
        'query': 'subtitle:"Breakout"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Panel (35)',
        'query': 'subtitle:"Panel"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Bootcamp (5)',
        'query': 'subtitle:"Bootcamp"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Certification',
        'query': 'subtitle:"Certification"',
        'category': 'next2019',
        'sort': 'title',
    },
]

NEXT19_LEARNING_LEVELS = [
    {
        'label': 'Introductory (144)',
        'query': 'subtitle:"Introductory"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Intermediate (186)',
        'query': 'subtitle:"Intermediate"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Advanced (71)',
        'query': 'subtitle:"Advanced"',
        'category': 'next2019',
        'sort': 'title',
    },
]

NEXT19_SESSION_TRACKS = [
    {
        'label': 'Application Development (37)',
        'query': 'subtitle:"Application Development"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Architecture (28)',
        'query': 'subtitle:"Architecture"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Collaboration & Productivity (42)',
        'query': 'subtitle:"Collaboration & Productivity"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Compute (23)',
        'query': 'subtitle:"Compute"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Cost Management (12)',
        'query': 'subtitle:"Cost Management"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Data Analytics (50)',
        'query': 'subtitle:"Data Analytics"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Databases (12)',
        'query': 'subtitle:"Databases"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'DevOps & SRE (18)',
        'query': 'subtitle:"DevOps & SRE"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Hybrid Cloud (35)',
        'query': 'subtitle:"Hybrid Cloud"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'IOT (20)',
        'query': 'subtitle:"IOT"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'ML & AI (42)',
        'query': 'subtitle:"ML & AI"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Mobility & Devices (21)',
        'query': 'subtitle:"Mobility & Devices"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Networking (15)',
        'query': 'subtitle:"Networking"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Security (44)',
        'query': 'subtitle:"Security"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Serverless (43)',
        'query': 'subtitle:"Serverless"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Storage (11)',
        'query': 'subtitle:"Storage"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Training & Certifications',
        'query': 'subtitle:"Training & Certifications"',
        'category': 'next2019',
        'sort': 'title',
    },
]

NEXT19_SESSION_INDUSTRIES = [
    {
        'label': 'Education (24)',
        'query': 'subtitle:"Education"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Energy (12)',
        'query': 'subtitle:"Energy"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Financial Services (28)',
        'query': 'subtitle:"Financial Services"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Gaming (17)',
        'query': 'subtitle:"Gaming"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Government (18)',
        'query': 'subtitle:"Government"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Healthcare (26)',
        'query': 'subtitle:"Healthcare"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Heavy Industrials (10)',
        'query': 'subtitle:"Heavy Industrials"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Manufacturing (23)',
        'query': 'subtitle:"Manufacturing"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Media & Entertainment (28)',
        'query': 'subtitle:"Media & Entertainment"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Oil & Gas (12)',
        'query': 'subtitle:"Oil & Gas"',
        'category': 'next2019',
        'sort': 'title',
    },
    {
        'label': 'Retail (33)',
        'query': 'subtitle:"Retail"',
        'category': 'next2019',
        'sort': 'title',
    },
]
