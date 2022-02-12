#!/bin/bash

: "${PROJECT_NAME:=home-credit}"

docker exec -i -t $PROJECT_NAME `echo "${@:1}"`

