#!/usr/bin/env bash

set -e

docker build -t edge_proxy_app-a:latest ./app-a &
docker build -t edge_proxy_app-b:latest ./app-b &
docker build -t edge_proxy_app-c:latest ./app-c &
docker build -t edge_proxy_envoy:latest ./envoy &

wait
