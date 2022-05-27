#!/bin/bash

# stop and remove container
docker stop home-credit-risk
docker rm home-credit-risk

# delete image
docker rmi home-credit-risk
