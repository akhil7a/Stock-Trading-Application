#! /bin/sh

# command to build catalog image
docker build -t catalog -f Dockerfile.catalog .
# command to build order image
docker build -t order -f Dockerfile.order .
# command to build frontend image
docker build -t frontend -f Dockerfile.frontend .

# Please note that this is just a script to build images