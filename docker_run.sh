#!/usr/bin/env bash

docker run --rm -it \
  --name mamuminna \
  --env TOKEN=$TOKEN \
  --env CONNECTION=$CONNECTION \
  --mount source=sql_persistance,target=/persistance \
  mamuminna:latest /bin/bash

