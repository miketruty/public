#!/usr/bin/env python

"""Script to locate and remove unused artifacts from our Cloud Run deployments.

My deploy workflow bundles sources files into a GCS bundle, then runs Cloud
Build to create a docker image in Artifact Registry, then uses that image
to create a new Cloud Run revision.
"""

import os
import sys

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from google.cloud import artifactregistry_v1
from google.cloud import run_v2
from google.cloud import storage


def prune_gcs_bundles(project_id, dt_cutoff):
    """Removes older gcs bundles from our deployment workflow.
    """
    bundles_removed = 0

    our_bucket = f'{project_id}_cloudbuild'
    print(f'Pruning GCS files older than {dt_cutoff} '
          f'from {our_bucket}...')

    storage_client = storage.Client(project=project_id)
    blobs = storage_client.list_blobs(our_bucket)
    for b in blobs:
        if b.time_created < dt_cutoff:
            print(f'prune {b.name}')
            print(f'  {b.time_created}')
            b.delete()
            bundles_removed += 1

    print(f'Pruned {bundles_removed} bundles from GCS.\n')


def prune_docker_images(project_id, repo_location, repo_name,
                        package_name, dt_cutoff):
    """Removes older docker images from our deployment workflow.
    """
    images_removed = 0

    parent = (f'projects/{project_id}/locations/{repo_location}/'
              f'repositories/{repo_name}/packages/{package_name}')

    client = artifactregistry_v1.ArtifactRegistryClient()
    page_result = client.list_versions(parent=parent)
    for response in page_result:
        if response.create_time < dt_cutoff:
            print(f'prune docker image version {response.name}')
            print(f'  {response.create_time}')
            del_response = client.delete_version(name=response.name)
            images_removed += 1

    print(f'Pruned {images_removed} docker image from our '
           'cloud-run-source-deploy artifact repo.\n')


def prune_cloud_run_revisions(project_id, service_location, service_name,
                              dt_cutoff):
    """Removes older Cloud Run revisions from our deployment workflow.
    """
    revisions_removed = 0

    parent = (f'projects/{project_id}/locations/{service_location}/'
              f'services/{service_name}')

    client = run_v2.RevisionsClient()
    page_result = client.list_revisions(parent=parent)
    for response in page_result:
        if response.create_time < dt_cutoff:
            print(f'prune Cloud Run revision {response.name}')
            print(f'  {response.create_time}')
            del_response = client.delete_revision(name=response.name)
            revisions_removed += 1

    print(f'Pruned {revisions_removed} revisions from Cloud Run.')


def main():
    """Do all the work.
    """
    project_id = os.getenv('CLOUD_PROJECT_ID')
    if not project_id:
        print(f'You must set the CLOUD_PROJECT_ID environment var!')
        sys.exit(-1)
    repo_location = 'us-west1'
    repo_name = 'cloud-run-source-deploy'
    package_name = 'test-dashboard-svc'
    service_location = 'us-west1'
    service_name = 'test-dashboard-svc'

    one_week_ago = datetime.utcnow() - timedelta(days=7)  # no timezone
    dt_cutoff = one_week_ago.replace(tzinfo=timezone.utc)  # with timezone

    prune_gcs_bundles(project_id, dt_cutoff)
    prune_docker_images(project_id, repo_location, repo_name, package_name,
                        dt_cutoff)
    prune_cloud_run_revisions(project_id, service_location, service_name,
                              dt_cutoff)


if __name__ == '__main__':
    main()
