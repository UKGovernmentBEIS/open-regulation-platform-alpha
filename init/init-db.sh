#!/bin/bash

#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

set +x
set +e

# export TERM=dumb
# red=`tput setaf 1`
# green=`tput setaf 2`
# reset=`tput sgr0`

run_scripts_in_dir() {
    ret_code=0
    for f in `find $1 -maxdepth 1 -type "f" -name "*.sql" | sort`
    do
        var_set=""
        for psql_var in $(grep -Po "[^:]:'?[\w_]+'?" $f | perl -pe "s/:'?([\w_]+)'?/\1/" | sort -u)
        do
            echo "file $f needs psql_var $psql_var"
            var_set="${var_set} -v ${psql_var}=${!psql_var}"
        done;
        # echo ${var_set}
        if basename ${f} | grep test; then
            echo "executing pgtap test ${f}"
            pg_prove -d ${POSTGRES_DB} -U postgres --ext .sql ${f}
            if [[ $? -eq 0 ]]; then
                echo "pgtap test ${f} passed";
            else
                echo "pgtap test ${f} failed";
                ret_code=1
            fi
        else
            echo "executing script ${f}"
            psql --username postgres --dbname ${POSTGRES_DB} -v "ON_ERROR_STOP=1" ${var_set} -f ${f}
            if [[ $? -ne 0 ]]; then
                echo "script ${f} failed"
                return 1
            fi
        fi
    done
    return $ret_code
}

echo "initialising schema"
run_scripts_in_dir "/ddl"
if [[ $? -eq 1 ]]; then
    echo "deploy failed"
    touch /var/lib/postgresql/deploy.failed
else
    echo "deploy success"
    touch /var/lib/postgresql/deploy.success
fi

if [ -f /var/lib/postgresql/deploy.success ]; then
    echo "installing python packages"
    for f in `ls /python`
    do
        echo "installing python packages ${f}"
        pip3 install /python/${f}/
        if [[ $? -ne 0 ]]; then
            echo "python package install failed"
            touch /var/lib/postgresql/setup.failed
            return 1
        fi
    done
    if [[ ${SKIP_SETUP} == "1" ]]; then
        echo "skipping setup"
        touch /var/lib/postgresql/setup.skipped
    else
        echo "running setup"
        run_scripts_in_dir "/setup"
        if [[ $? -eq 1 ]]; then
            echo "setup failed"
            touch /var/lib/postgresql/setup.failed
        else
            echo "setup succeded"
            touch /var/lib/postgresql/setup.success
        fi
    fi

    if [[ ${RUN_TESTS} == "1" ]]; then
        echo "running test setup"
        run_scripts_in_dir "/tests/setup"
        echo "running tests"
        run_scripts_in_dir "/tests"
        if [[ $? -eq 1 ]]; then
            echo "some tests failed"
            touch /var/lib/postgresql/pgtap_tests.failed
        else
            echo "all tests passed"
            touch /var/lib/postgresql/pgtap_tests.passed
        fi
        echo "pgtap tests complete"
    fi

fi




