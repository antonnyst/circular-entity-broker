# How to use

## API Endpoints (for internal control only, not meant to be a public API):
```
GET   /invoke/register - register fake_company with the broker, returns access token
GET   /invoke/unregister - delete all products and request fake_company to be removed from the broker
GET   /invoke/create?amount=X - generate X amount of new products (returns copies of the new products as json)
GET   /invoke/update?amount=X - change the description of X amount of random products
GET   /invoke/delete?amount=X - delete X amount of random products
GET   /products - get all products currently belonging to fake_company
```

## Workflow

1. FakeCompany registers with broker
2. FC creates products with all metadata
3. Broker interrogates occasionally about "fluid" product data (stock, price etc.)
4. FakeCompany updates broker when product metadata changes
