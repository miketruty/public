## SETUP

You must setup 2 things to run this application on App Engine:

1.  Authentication (client_secrets.json).
2.  Common library files.

### Authentication Setup

You should generate and download a web-client client_secrets.json file from the
GCP Console > APIs & Services > Credentials > OAuth 2.0 client IDs.

When generating, you should supply the following as authorized redirect URIs
(where appname might be `gcp-next-reviewdeo.appspot.com`):

*   `https://[appname]/oauth2callback`
*   `http://localhost:8080/oauth2callback`
*   `https://cloud-next-library.googleplex.com/oauth2callback`

You should then download as a `client_secret_*.json` file from the credentails
page. The downloaded file should be renamed client_secrets.json and placed in
the src directory alongside the app.yaml file.

### Common Library Setup

You must setup a lib directory under src with some libraries including the
Python Google API Client and the App Engine Cloud Storage library. This is
explained in the
[Google Developers pages here](https://developers.google.com/api-client-library/python/start/installation)
and the App Engine parts more specifically described in
[vendoring into your application](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27#vendoring).

One way to consider:

```
$ cd ./src
$ mkdir ./lib
$ pip install -t lib -r requirements.txt
```

As of 2018 the lib directory looked something like this:

```
GoogleAppEngineCloudStorageClient-1.9.22.1-py2.7.egg-info/
apiclient/
cloudstorage/
google_api_python_client-1.6.2.dist-info/
googleapiclient/
httplib2-0.10.3-py2.7.egg-info/
httplib2-0.10.3.dist-info/
httplib2/
oauth2client-4.0.0.dist-info/
oauth2client/
pyasn1-0.2.3.dist-info/
pyasn1/
pyasn1_modules-0.0.8.dist-info/
pyasn1_modules/
rsa-3.4.2.dist-info/
rsa/
six-1.10.0.dist-info/
tests/
uritemplate-3.0.0.dist-info/
uritemplate/
six.py*
```

As of 2020 the lib directory looked like this:

```
GoogleAppEngineCloudStorageClient-1.9.22.1.dist-info/
__pycache__/
apiclient/
bin/
cachetools-4.1.0.dist-info/
cachetools/
certifi-2020.4.5.2.dist-info/
certifi/
chardet-3.0.4.dist-info/
chardet/
cloudstorage/
google/
google_api_core-1.20.0.dist-info/
google_api_python_client-1.9.3.dist-info/
google_auth-1.17.2.dist-info/
google_auth_httplib2-0.0.3.dist-info/
googleapiclient/
googleapis_common_protos-1.52.0.dist-info/
httplib2-0.18.1.dist-info/
httplib2/
idna-2.9.dist-info/
idna/
pkg_resources/
protobuf-3.12.2.dist-info/
pyasn1-0.4.8.dist-info/
pyasn1/
pyasn1_modules-0.2.8.dist-info/
pyasn1_modules/
pytz-2020.1.dist-info/
pytz/
requests-2.23.0.dist-info/
requests/
rsa-4.6.dist-info/
rsa/
setuptools-47.1.1.dist-info/
setuptools/
six-1.15.0.dist-info/
uritemplate-3.0.1.dist-info/
uritemplate/
urllib3-1.25.9.dist-info/
urllib3/
easy_install.py
google_api_core-1.20.0-py3.8-nspkg.pth
google_auth-1.17.2-py3.8-nspkg.pth
google_auth_httplib2.py
googleapis_common_protos-1.52.0-py3.8-nspkg.pth
protobuf-3.12.2-py3.7-nspkg.pth
six.py
```
