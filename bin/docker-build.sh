#!/bin/bash
: "${PROJECT_NAME:=home-credit-risk}"

docker build --no-cache -t nastjamakh/$PROJECT_NAME:latest .
