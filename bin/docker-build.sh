#!/bin/bash
: "${PROJECT_NAME:=home-credit-risk}"

docker build --no-cache --platform linux/amd64 -t $PROJECT_NAME .
