# /database

The database we use is [GraphDB](https://graphdb.ontotext.com/documentation/10.8/) and this directory simply contains an Dockerfile for running an instance of it.

After proper running and setup as explained in the root directory [README.md](../README.md) the database will contain the schema and metadata about the companies products

## Endpoints
The broker interfaces with the database using the following endpoints

For select queries:  
`POST /repositories/<REPO_NAME>`

For update queries  
`POST /repositories/<REPO_NAME>/statements`

## Running
Should be run together with the broker and website using the docker-compose setup and instructions in the root directory [README.md](../README.md).