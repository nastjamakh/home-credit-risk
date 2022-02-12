#!/bin/bash

: "${PROJECT_NAME:=home-credit}"

if  docker ps | grep " $PROJECT_NAME$"; then
    docker kill $PROJECT_NAME
fi

if docker ps -a |grep " $PROJECT_NAME$" ; then
    docker rm $PROJECT_NAME
fi
