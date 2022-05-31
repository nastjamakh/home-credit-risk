#!/bin/bash

: "${PROJECT_NAME:=home-credit-risk}"

docker exec -i $PROJECT_NAME `echo "${@:1}"`

