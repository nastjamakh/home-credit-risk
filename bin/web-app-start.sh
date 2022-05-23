#!/bin/bash

# download latest model from S3
docker exec -i home-credit-risk /bin/bash -c "export API_KEY=foo"
docker exec -d -i home-credit-risk poetry run uvicorn api:app --host 0.0.0.0