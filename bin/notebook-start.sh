#!/bin/bash
: "${PROJECT_NAME:=home-credit-risk}"

docker exec -i -t  ${PROJECT_NAME} \
  poetry run dotenv run jupyter notebook \
  --ip="*" \
  --port=7777 \
  --NotebookApp.token=''  \
  --NotebookApp.custom_display_url=http://localhost:7777
