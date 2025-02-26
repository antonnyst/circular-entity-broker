# circular-entity-broker

An metadata broker for product search.

## Architecture

### /docs
Contains documentation

### /broker
The middleman between users and the database.

Converts requests into SPARQL queries to the database and interprets results to respond to the requests.

### /web
The website for user interaction.

Allows for the search of products etc

### /fake-company
An mock company for testing and demonstration purposes.

Can randomly generate products, add, modify and remove them, as well as respond to interrogation requests from the broker.

### /database
This folder simply contains a Dockerfile for running the database.

### /rdf
The initial rdf data and schema. The data is stored in the .ttl format 


## Running

Before trying to run the project make sure [Docker Compose](https://docs.docker.com/compose/) is installed and running on your system.

To start the project, simply run the following command in the project base directory:

`docker compose up`

> [!IMPORTANT]
> After starting the project with an empty graph database,
> a new graphDB repository needs to be created and the initial rdf schema imported.
> See [DBINIT.md](database/DBINIT.md).
