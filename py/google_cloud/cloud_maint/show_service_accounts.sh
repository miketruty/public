#!/usr/bin/env zsh


# Show service accounts

set -x

echo '**Service Accounts**'
gcloud iam service-accounts list

# REFERENCE
#
# TO CREATE:
# gcloud iam service-accounts create vnv-test-data-firestore-writer --display-name vnv-test-data-firestore-writer
