#!/bin/bash
: "${PROJECT_NAME:=home-credit}"

docker build --no-cache -t $PROJECT_NAME:latest .
