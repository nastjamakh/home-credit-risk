#!/bin/bash

# delete all containers
docker rm -vf $(docker ps -aq)

# delete all images
docker rmi -f $(docker images -aq)

# gi to project directory
cd home-credit-risk