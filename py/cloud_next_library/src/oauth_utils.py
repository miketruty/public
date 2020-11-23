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
"""Setup for OAuth2.
"""

import os

from oauth2client.contrib.appengine import CredentialsModel
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
from oauth2client.contrib.appengine import StorageByKeyName

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
YOUTUBE_READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/youtube'

decorator = OAuth2DecoratorFromClientSecrets(CLIENT_SECRETS,
                                             YOUTUBE_READ_WRITE_SCOPE)


def _CreateStorage(key_name):
  return StorageByKeyName(
      model=CredentialsModel,
      key_name=key_name,  # Use user_id.
      property_name='credentials')


def AddCredentialsToStorage(key_name, credentials):
  _CreateStorage(key_name).put(credentials)


def GetCredentialsFromStorage(key_name):
  return _CreateStorage(key_name).get()
