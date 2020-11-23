#!/bin/bash

for f in ./schema/*.yaml; do
  echo "$f" && go run . yamltojson "$f"  > "${f%.yaml}.json"
done
