#!/usr/bin/env python

"""Script to locate and list artifacts from our Cloud Run deployments.

Our deploy workflow bundles sources files into a GCS bundle, then runs Cloud
Build to create a docker image in Artifact Registry, then uses that image
to create a new Cloud Run revision.
"""

from google.cloud import artifactregistry_v1
from google.cloud import run_v2
from google.cloud import storage


def show_gcs_bundles(project_id):
    """Cleanly show gcs bundles from our deployment workflow.
    """
    our_bucket = f'{project_id}_cloudbuild'
    print(f'Showing GCS files from {our_bucket}...')

    storage_client = storage.Client(project=project_id)
    blobs = storage_client.list_blobs(our_bucket)
    for b in blobs:
        print(f'{b.name}, {b.time_created}')
    print()


def show_docker_images(project_id):
    """Cleanly show docker images from our deployment workflow.

    Note: these seem to be disordered.
    """
    repo_location = 'us-west1'
    repo_name = 'cloud-run-source-deploy'
    package_name = 'test-dashboard-svc'
    parent = (f'projects/{project_id}/locations/{repo_location}/'
              f'repositories/{repo_name}/packages/{package_name}')
    print(f'Showing docker images from Artifact Registry from '
          f'{repo_name}/{package_name}...')

    client = artifactregistry_v1.ArtifactRegistryClient()
    page_result = client.list_versions(parent=parent)
    for response in page_result:
        print(f'{response.name}, {response.create_time}')
    print()


def show_cloud_run_revisions(project_id):
    """Cleanly show Cloud Run revisions from our deployment workflow.
    """
    service_location = 'us-west1'
    service_name = 'test-dashboard-svc'
    parent = (f'projects/{project_id}/locations/{service_location}/'
              f'services/{service_name}')
    print(f'Showing Cloud Run revisions from {service_name}...')

    client = run_v2.RevisionsClient()
    page_result = client.list_revisions(parent=parent)
    for response in page_result:
         print(f'{response.name}, {response.create_time}')


def main():
    """Do all the work.
    """
    vnv_project_id = 'dev-us-5g-vnvtestdata-1'

    show_gcs_bundles(vnv_project_id)
    show_docker_images(vnv_project_id)
    show_cloud_run_revisions(vnv_project_id)


if __name__ == '__main__':
    main()
