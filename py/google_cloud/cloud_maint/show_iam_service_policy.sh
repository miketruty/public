#!/usr/bin/env zsh

# Show IAM service account for Cloud Run service.

set -x

gcloud run services get-iam-policy test-dashboard-svc

# Remove the policy.
# gcloud run services remove-iam-policy-binding test-dashboard-svc \
#     --member "serviceAccount:vnv-test-data-dashboard-app@dev-us-5g-vnvtestdata-1.iam.gserviceaccount.com" \
#     --role "roles/run.invoker"

# Add the policy.
# gcloud run services add-iam-policy-binding test-dashboard-svc \
#     --member "serviceAccount:vnv-test-data-dashboard-app@dev-us-5g-vnvtestdata-1.iam.gserviceaccount.com" \
#     --role "roles/run.invoker"

# Users who deploy the service will need this.
# gcloud iam service-accounts add-iam-policy-binding "vnv-test-data-dashboard-app@dev-us-5g-vnvtestdata-1.iam.gserviceaccount.com" \
#     --member "user:michael.truty@dexcom.com" \
#     --role "roles/iam.serviceAccountUser"
