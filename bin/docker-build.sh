#!/bin/bash
: "${PROJECT_NAME:=home-credit}"

docker build -t $PROJECT_NAME:latest .
