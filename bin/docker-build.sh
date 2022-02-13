#!/bin/bash
: "${PROJECT_NAME:=home-credit}"

docker build --no-cache -t nastjamakh/$PROJECT_NAME:latest .
