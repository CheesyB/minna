#!/usr/bin/env bash

docker run --rm -d \
  --name mamuminna \
  --env TOKEN=$TOKEN \
  --env CONNECTION=$CONNECTION \
  --mount source=sql_persistance,target=/persistance \
  mamuminna:latest 

