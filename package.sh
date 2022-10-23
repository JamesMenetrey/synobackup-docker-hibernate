#!/usr/bin/env bash

docker build . -t synobackup-docker-hibernate
docker run --rm -v "$(pwd):/src" synobackup-docker-hibernate