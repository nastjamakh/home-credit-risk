#!/bin/bash

# download latest model from S3
docker exec -d -i home-credit-risk poetry run uvicorn api:app --host 0.0.0.0