#!/bin/bash

#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
#

# download demo files into demo_data directory

FILE=demo_data
if [ -d "$FILE" ]; then
    echo "Rewriting $FILE."
    rm -r demo_data
    wget https://orp-alpha-demo-data.s3.eu-west-2.amazonaws.com/demo_data.zip
    unzip demo_data.zip
    rm demo_data.zip
else
    wget https://orp-alpha-demo-data.s3.eu-west-2.amazonaws.com/demo_data.zip
    unzip demo_data.zip
    rm demo_data.zip
fi