# /broker

The broker acts as an middleman between the web/companies and the graphDB database.

Built using python flask primarily and bundled in the Dockerfile.

## Endpoints
The broker is interfaced using an HTTP API defined by the [Swagger](https://swagger.io/) API specification in [openapi.yaml](openapi.yaml).

## Running
Should be run together with the database and website using the docker-compose setup and instructions in the root directory [README.md](../README.md).