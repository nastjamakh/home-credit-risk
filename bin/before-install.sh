#!/bin/bash

# delete all containers
docker container prune -f

# delete all images
docker image prune -f
