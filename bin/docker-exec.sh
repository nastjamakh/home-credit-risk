#!/bin/bash

: "${PROJECT_NAME:=home-credit-risk}"

docker exec -i -t $PROJECT_NAME `echo "${@:1}"`

