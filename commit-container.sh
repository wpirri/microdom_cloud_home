#!/bin/sh

docker build -t microdom-cloud-home:latest .
docker tag microdom-cloud-home:latest ghcr.io/wpirri/microdom-cloud-home:latest
docker push ghcr.io/wpirri/microdom-cloud-home:latest

