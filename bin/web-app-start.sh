#!/bin/bash

# download latest model from S3
API_KEY=foo  PYTHONPATH=${PWD}/src docker exec -i home-credit-risk poetry run uvicorn api:app --reload --port 8012 --host 0.0.0.0