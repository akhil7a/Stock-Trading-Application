#! /bin/sh

# command to build catalog image
docker build -t catalog -f Dockerfile.catalog .
# command to build order image
docker build -t order -f Dockerfile.order .
# command to build frontend image
docker build -t frontend -f Dockerfile.frontend .

# Please note that this is just a script to build images

# run catalog service
docker run --name catalog_service -p 8088:8088 -v /"$(pwd)"/src/backend/catalog/db.json:/db.json -d catalog

CATALOG_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' catalog_service)

# run order service
docker run --name order_service -e CATALOG_HOST="$CATALOG_HOST" -v /"$(pwd)"/src/backend/order/log.json:/log.json -p 8089:8089 -d order

ORDER_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' order_service)

# run frontend service
docker run --name frontend_service -e CATALOG_HOST="$CATALOG_HOST" -e ORDER_HOST="$ORDER_HOST" -p 3010:3010 -d frontend