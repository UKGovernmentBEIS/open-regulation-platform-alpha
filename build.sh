#!/bin/bash

#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
docker pull postgres:13
docker build -q -t postgres-orp:13 -f Dockerfile.pg .
docker build -q -t consumer-api-orp:latest -f external-apis/Dockerfile external-apis
# comment line below for local build
docker build --no-cache -q -t editorial-ui-orp:latest --build-arg API_BASE_URL=/ -f editorial-ui/Dockerfile editorial-ui
# uncomment below for local build
# docker build --no-cache -q -t editorial-ui-orp:latest --build-arg API_BASE_URL=http://localhost:3001/ -f editorial-ui/Dockerfile editorial-ui
docker pull subzerocloud/pg-amqp-bridge:0.0.8
docker pull rabbitmq:3.9.8-management
docker build -q -t postgres-orp:13 -f Dockerfile.pg .
docker build -q -t orp-email-consumer:0.1 -f event_consumer/Dockerfile.event_consumer ./event_consumer
docker build -q -t api-documentation-orp:latest -f documentation-visualisation-artifacts/artifacts/orp-documentation/Dockerfile documentation-visualisation-artifacts/artifacts/orp-documentation
docker build -q -t graph-visualisation-orp:latest -f documentation-visualisation-artifacts/artifacts/orp-graph-visualisation/Dockerfile documentation-visualisation-artifacts/artifacts/orp-graph-visualisation
