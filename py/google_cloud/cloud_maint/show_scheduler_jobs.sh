#!/usr/bin/env zsh

# Show scheduler jobs

set -x

echo '**Scheduler jobs**'
gcloud scheduler jobs list --location=us-west1
