#!/bin/bash

source colours.sh

set -e

temp_env_dir=$(mktemp -d)
virtualenv ${py3_env} ${temp_env_dir} > /dev/null 2>&1
source ${temp_env_dir}/bin/activate
pip -q install pytest requests lxml arrow psycopg2-binary

i=0
until http --quiet --quiet --check-status POST 127.0.0.1:3001/rpc/login email=editor@beis.gov.uk password=Password1\! 2>/dev/null
do
    echo "stack not ready yet"
    sleep 15
    i=$((i+1))
    if [[ $i -ge 20 ]]; then
        red "giving up"
        exit 1
    fi;
done

green "stack is ready"
sleep 20
echo "running pytests"


pytest python/orp/orp/xmltools
pytest python/orp/orp/content_enrichment
pytest python/orp/orp/authority_ner
pytest tests/api_tests/pytests
pytest tests/pytests

rm -r ${temp_env_dir}