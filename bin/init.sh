#!/bin/bash

# download latest model from S3
docker exec -i home-credit-risk poetry run model load_from_s3