#!/usr/bin/env zsh

# Create scheduler jobs

set -x

# Create commands

# NOTE: 3min is the default Cloud Run deadline - after which it kills the job.

# Get projects 12:01a PST
gcloud scheduler jobs create http daily-get-projects --location=us-west1 \
    --schedule "1 0 * * *" \
    --uri "https://test-dashboard-svc.dexcomdev.com/admin/results/0.Projects" \
    --http-method get \
    --time-zone "America/Los_Angeles" \
    --attempt-deadline 3m

# Get CAMS results 01:02a PST
gcloud scheduler jobs create http daily-get-cams --location=us-west1 \
    --schedule "2 1 * * *" \
    --uri "https://test-dashboard-svc.dexcomdev.com/admin/results/11.Results" \
    --http-method get \
    --time-zone "America/Los_Angeles" \
    --attempt-deadline 15m


# Get projects 02:03a PST
gcloud scheduler jobs create http daily-get-udp --location=us-west1 \
    --schedule "3 2 * * *" \
    --uri "https://test-dashboard-svc.dexcomdev.com/admin/results/12.Results" \
    --http-method get \
    --time-zone "America/Los_Angeles" \
    --attempt-deadline 15m


# Get G7 results 03:04a PST
gcloud scheduler jobs create http daily-get-g7 --location=us-west1 \
    --schedule "4 3 * * *" \
    --uri "https://test-dashboard-svc.dexcomdev.com/admin/results/1.Results" \
    --http-method get \
    --time-zone "America/Los_Angeles" \
    --attempt-deadline 15m


# Get SDK 04:05a PST
gcloud scheduler jobs create http daily-get-sdk --location=us-west1 \
    --schedule "5 4 * * *" \
    --uri "https://test-dashboard-svc.dexcomdev.com/admin/results/3.Results" \
    --http-method get \
    --time-zone "America/Los_Angeles" \
    --attempt-deadline 3m
