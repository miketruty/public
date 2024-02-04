#!/usr/bin/env zsh

# Mount my image so I can look at the files.
IMAGEURL="us-west1-docker.pkg.dev/dev-us-5g-vnvtestdata-1/cloud-run-source-deploy/flask_localdash:latest"
docker run -it --rm "$IMAGEURL" bash
