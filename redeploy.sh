#!/bin/bash

#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#


docker stack down orp-alpha > /dev/null 2>&1
while docker stack ls | grep orp-alpha
do
    echo "waiting for stack to down"
    sleep 2
done

echo "old stack is down"

sleep 2

./deploy.sh