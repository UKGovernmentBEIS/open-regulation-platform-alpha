#!/bin/bash

#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

source colours.sh

SKIP_SETUP=1 RUN_TESTS=1 ./redeploy.sh

if [[ $? -ne 0 ]]; then
    exit 1
fi


until docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/pgtap_tests.*"
do
    echo "waiting for pgtap status"
    sleep 10
done

docker logs $(docker ps -q --filter name=orp-alpha_db) 2>&1 | grep -iE '(^/tests/.+\.sql)|(pgtap tests complete)'

if docker exec $(docker ps -q --filter name=orp-alpha_db) sh -c "test -f /var/lib/postgresql/pgtap_tests.failed";
then
    red "pgtap failed"
    docker logs $(docker ps -q --filter name=orp-alpha_db) 2>&1 | grep -E -B 100 "Failed [0-9]+/[0-9]+ subtests" | grep -iE '(^#)|(ERROR)'
    exit 1
fi

green "pgtap success"

if [[ ${SKIP_PYTESTS} == "1" ]]; then
    echo "skipping pytests"
else
    echo "deploying again for pytests"
    ./redeploy.sh && ./run_pytests.sh
fi


