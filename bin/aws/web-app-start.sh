#!/bin/bash

# download latest model from S3
docker exec -i -d home-credit-risk poetry run uvicorn api:app --port=8012 --host 0.0.0.0