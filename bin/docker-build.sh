#!/bin/bash
: "${PROJECT_NAME:=home-credit-risk}"

docker build --no-cache -t $PROJECT_NAME:latest .
