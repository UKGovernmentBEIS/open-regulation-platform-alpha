#!/bin/bash

ADDRESS="127.0.0.1"

while getopts ":a:" opt; do
    case "$opt" in
    a)
        ADDRESS=$OPTARG
        ;;
    esac
done

streamlit run toc.py -- -a $ADDRESS &
streamlit run login.py --server.port=8502 --server.baseUrlPath=login &
streamlit run browse.py --server.port=8503 --server.baseUrlPath=browse &
streamlit run search.py --server.port=8504 --server.baseUrlPath=search &
streamlit run context1.py --server.port=8505 --server.baseUrlPath=context1 &
streamlit run monitor.py --server.port=8506 --server.baseUrlPath=monitor &
streamlit run explore.py --server.port=8507 --server.baseUrlPath=explore &
streamlit run enrich.py --server.port=8508 --server.baseUrlPath=enrich &

wait