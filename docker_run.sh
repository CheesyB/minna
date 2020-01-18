#!/usr/bin/env bash

docker run --rm -d \
  --name mamuminna \
  --env TOKEN=$TOKEN \
  --env CONNECTION=$CONNECTION \
  --env LOGPATH=$LOGPATH \
  --env LOGNAME=$LOGNAME \
  --mount source=sql_persistance,target=/persistance \
  mamuminna:latest 

