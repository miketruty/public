#!/usr/bin/env bash

# Easiest way to get an identity token for the service, with a custom audience.

gcloud auth activate-service-account --key-file="$HOME/vnvtestdata_firestore_writer.json"
export TOKEN=$(gcloud auth print-identity-token --audiences="478061995323-0gvgnjkochgc91gf276jkten1lcegcke.apps.googleusercontent.com")
curl -H "Authorization: Bearer $TOKEN" https://dexcom-vnv-testrail-webhook.dexcomdev.com
