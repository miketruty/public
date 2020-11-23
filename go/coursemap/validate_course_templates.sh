#!/bin/bash

if [[ ! -f coursemap ]]
then
  go build .
fi

find ~/src/github.com/CloudVLab/gcp-ondemand-content/course_templates/ -type f -iname 'qwiklabs.yaml' -exec ./coursemap validate {} \;
