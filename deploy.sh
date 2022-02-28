#!/bin/bash

#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

set -euo pipefail

source colours.sh

./build.sh
./load_data.sh


export BASE_DIR=$(pwd)
until docker stack up orp-alpha -c docker-compose.yml > /dev/null 2>&1
do
    echo "trying stack deploy again"
    sleep 2
done

green "stack deploy success"

until docker ps -q --filter name=orp-alpha_db | wc -l | grep 1 > /dev/null 2>&1
do
    echo "waiting for db container"
    sleep 2
done


green "db container up"


until docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/deploy.*"
do
    echo "waiting for deployment status"
    sleep 10
done

if docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/deploy.failed";
then
    red "deploy failed"
    docker logs $(docker ps -q --filter name=orp-alpha_db) 2>&1 | grep -B 30 "deploy failed"
    exit 1
fi

green "deploy success"


until docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/setup.*"
do
    echo "waiting for setup status"
    sleep 10
done

if docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/setup.failed";
then
    red "setup failed"
    docker logs $(docker ps -q --filter name=orp-alpha_db) 2>&1 | grep -B 30 "setup failed"
    exit 1
fi

if docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/setup.skipped";
then
    green "setup skipped"
else
    green "setup success"
fi






# docker service logs --follow orp-alpha_db