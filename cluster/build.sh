#!/usr/bin/env bash

set -e

docker build -t edge_proxy_app-a:v1.0.1 ./app-a &
docker build -t edge_proxy_app-b:v1.0.1 ./app-b &
docker build -t edge_proxy_app-c:v1.0.1 ./app-c &
docker build -t edge_proxy_envoy:v1.0.1 ./envoy &

wait
