# Fakecompanies 
Fake-companies is used as testing data so we can test how the broker works without the need of existing companies. 


# How to use

## Start fakecompanies 
Don't forget to start GraphDB!
```
$ cd circular-entity-broker/fake-company/
$ flask --app fake_company run
```
## API Endpoints (for internal control only, not meant to be a public API):
```
GET   /invoke/register - register fake_company with the broker, returns access token
GET   /invoke/unregister - delete all products and request fake_company to be removed from the broker
POST  /invoke/set_interrogation - register a url, set in the JSON body as parameter 'url' (port is added by fake_company), with the broker for interrogation
POST  /invoke/unset_interrogation - unregister a url, set in the JSON body as parameter 'url' (port is added by fake_company), from the broker
GET   /invoke/create?amount=X - generate X amount of new products (returns copies of the new products as json)
GET   /invoke/update?amount=X - change the description of X amount of random products
GET   /invoke/remove?amount=X - delete X amount of random products
GET   /products - get all products currently belonging to fake_company

GET   /invoke/setup - shorthand to register, set_interrogation and create 3 products
```

## Workflow

1. FakeCompany registers with broker
2. FC creates products with all metadata
3. Broker interrogates occasionally about "fluid" product data (stock, price etc.)
4. FakeCompany updates broker when product metadata changes
