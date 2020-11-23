# Full-Text Search App: Video Search

## Introduction

This Python App Engine application illustrates the use of the [Full-Text Search
API](https://developers.google.com/appengine/docs/python/search) in a "Video
Search" domain.

## Configuration

Before you deploy the application, edit `app.yaml` to specify your own app id
and version.

## Information About Running the App Locally

Log in as an app admin to add and modify the app's video data.

The app uses XG (cross-group) transactions, which requires the dev_appserver to
be run with the `--high_replication` flag. E.g., to start up the dev_appserver
from the command line in the project directory (this directory), assuming the
GAE SDK is in your path, do:

    dev_appserver.py --high_replication .

The app is configured to use Python 2.7. On some platforms, it may also be
necessary to have Python 2.7 installed locally when running the dev_appserver.

When running the app locally, not all features of the search API are supported.
So, not all search queries may give the same results during local testing as
when run with the deployed app. Be sure to test on a deployed version of your
app as well as locally.

## Administering the deployed app

You will need to be logged in as an administrator of the app to add and modify
video data, though not to search videos or add reviews. If you want to remove
this restriction, you can edit the `login: admin` specification in `app.yaml`,
and remove the `@BaseHandler.admin` decorators in `admin_handlers.py`.

## Updating video documents with a new average rating

When a user creates a new review, the average rating for that product is updated
in the datastore. The app may be configured to update the associated product
`search.Document` at the same time (the default), or do this at a later time in
batch (which is more efficient). See `cron.yaml` for an example of how to do
this update periodically in batch.

## Searches

Any valid queries can be typed into the search box. This includes simple word
and phrase queries, but you may also submit queries that include references to
specific document fields and use numeric comparators on numeric fields. See the
Search API's
[documentation](https://developers.google.com/appengine/docs/python/search) for
a description of the query syntax.
