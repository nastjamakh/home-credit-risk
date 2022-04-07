#!/bin/bash
: "${PROJECT_NAME:=home-credit-risk}"

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/i9f8r4q1
docker pull public.ecr.aws/i9f8r4q1/$PROJECT_NAME:latest
docker tag public.ecr.aws/i9f8r4q1/$PROJECT_NAME:latest $PROJECT_NAME:latest