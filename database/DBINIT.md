# Instruction for starting GraphDB

## Start docker
`docker-compose up`

## Open web browser of your choice and go to Graphdb (firefox recommended)
Enter: `localhost:7200`

![Localhost:7200](../docs/images/Mon%20Mar%20%203%2004:39:54%20PM%20CET%202025.png)


Here Click on `Import` and then `Create new repository` next to the plus sign. 

Then click on `GraphDB repository`

Here you want to enter `ceb` as the repositoryID as seen below and then click on `create` at bottom right of the page

![Create grapghDB repo](../docs/images/GraphDBThingamathings.png)

### Importing the server data to graphDB repo

click on ceb repository
![click me pls](../docs/images/clickCEB.png)

And then on `import rdf data`

Now click on the `Server files` tab and select all and then click on `import`

Leave the import settings as default and it should look like as seen in the picture below:
![Import data settigns](../docs/images/graphDbImportSettings.png)

If everyting looks right you can click on import. 

## Test if import actually worked 

Click on the SparQL tab on the left and run the default query. If the query for some reason is not autofilled you can copy it from here: 
```PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX cmp: <http://ceb.ltu.se/components/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select * where {
    ?s ?p ?o .
} limit 10000
```

If everything is done correctly it should look something like this: 
![GraphDB Result](../docs/images/graphDBResult.png)