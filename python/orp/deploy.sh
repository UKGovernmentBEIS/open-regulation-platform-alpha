#!/bin/bash
#
#   Copyright (C) 2020 Liam Brannigan
#
#Target can be 'dev', 'lab' or 'app' to run with an open port for the notebook or streamlit apps
TARGET=$1
BUILD_TARGET=$1
if [ "${TARGET}" == "app" ]; then
  BUILD_TARGET=dev
fi
show_help() {
    echo "Deploy docker image in dev, or lab mode. Same image is built in both cases, but lab argument opens a port from the container"
    echo ""
    echo "USAGE:"
    echo "    ./deploy.sh [-i TARGET]"
    echo ""
    echo "OPTIONAL ARGUMENTS:"
    echo "    -i TARGET"
    echo "        The stage of the Dockerfile to build to (default = dev)"
    exit 0
}

DOCKER_BUILDKIT=1 docker build -t orp-content-enrichment .
# # Mount directory 2 levels up to access data directory inside container
# # Docker requires absolute path for mounts, so need absolute path on host machine
# current_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
# echo ${current_path}
# for i in {1..2}
#   do
#   current_path=$( cd "$(dirname "${current_path}")" ; pwd -P )
# done


docker run  -it -p 8888:8888 --rm -v $(pwd):/usr/src/app orp-content-enrichment:latest /bin/bash

