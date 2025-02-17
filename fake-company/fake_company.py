from flask import Flask, request, jsonify
import requests, sys
from product import Sawblade
from company import FakeCompany
import json

app = Flask(__name__)

# TEMP: Hard-coded config values
BROKER_URL = "http://localhost:7100"
company = FakeCompany()
print("Created FakeCompany with name", company.name)

## API Endpoints (for internal control only, not meant to be a public API):
# GET   /invoke/register - register fake_company with the broker, returns access token
# GET   /invoke/unregister - delete all products and request fake_company to be removed from the broker
# GET   /invoke/create?amount=X - generate X amount of new products (returns copies of the new products as json)
# GET   /invoke/update?amount=X - change the description of X amount of random products
# GET   /invoke/delete?amount=X - delete X amount of random products
# GET   /products - get all products currently belonging to fake_company
# 
# GET   /api/fluid_data?pid=X - get fluid data (stock/price) for product with product id = X

@app.route("/")
def hello_world():
  return f"<h1>{company.name}</h1>"

# TODO: Not implemented in broker yet
@app.get("/invoke/register")
def invoke_registration():
  # Invoke a registration with the broker. This should only be used once after startup
  if company.registered:
    return "Already registered", 400
  
  # Send request to broker
  json = {"name": company.name}
  response = requests.post(BROKER_URL + "/register", json)
  data = response.json()
  access_token = data["accessToken"]
  company_id = data["companyId"]
  # print("Registered, access token:", access_token)

  if response.status_code == 200:
    company.access_token = access_token
    company.id = company_id
    company.registered = True

  return access_token

# TODO: Not implemented in broker yet
@app.get("/invoke/unregister")
def invoke_unregistration():
  # Invoke an unregistration with the broker. This will remove all company data and products from the broker
  if not company.registered:
    return "Not registered", 400
  
  # Send request to broker
  headers = {"X-API-CAT": company.access_token}
  requests.delete(BROKER_URL + "/register", headers)

  return "Unregistered"


# Invoke fake_company to create X amount of new randomized products
@app.get("/invoke/create")
def invoke_product_creation():
  # TODO: Not implemented in broker yet
  # if not company.registered:
  #   return "Not registered", 400
  
  new_products = company.generateProducts(int(request.args.get("amount")))
  company.products.extend(new_products)
  new_product_jsons = []
  for product in new_products:
    json = {"properties": product.toProperties()}
    headers = {"X-API-CAT": company.access_token}
    response = requests.post(BROKER_URL + "/product", json=json, headers=headers)
    product.id = response.json()["productId"]
    new_product_jsons.append(product.toObject())

  return new_product_jsons

# Invoke fake_company to update X amount of random products
@app.get("/invoke/update")
def invoke_product_update():
  # TODO: Not implemented in broker yet
  # if not company.registered:
  #   return "Not registered", 400
  
  updated_products = company.updateProducts(int(request.args.get("amount")))
  updated_product_jsons = []
  for product in updated_products:
    json = {"properties": product.toProperties()}
    headers = {"X-API-CAT": company.access_token}
    requests.put(BROKER_URL + "/product?productId=" + product.id, json=json, headers=headers)
    updated_product_jsons.append(product.toObject())

  return updated_product_jsons

# Invoke fake_company to remove X amount of random products
@app.get("/invoke/remove")
def invoke_product_remove():
  # TODO: Not implemented in broker yet
  # if not company.registered:
  #   return "Not registered", 400
  
  removed_products = company.removeProducts(int(request.args.get("amount")))
  removed_product_jsons = []
  for product in removed_products:
    headers = {"X-API-CAT": company.access_token}
    requests.delete(BROKER_URL + "/product?productId=" + product.id, headers=headers)
    removed_product_jsons.append(product.toObject())

  return removed_product_jsons



# Return all stored products (mainly for debug purposes)
@app.route("/products")
def all_products():
  products = []
  for product in company.products:
    products.append(product.toObject())
  return products


# Serve fluid data to the broker
@app.route("/api/fluid_data")
def fluid_data():
  # Get product id from path param "pid"
  pid = request.args.get("pid", "")
  if pid != "":
    # Find product and return its fluid data
    for product in company.products:
      if product.product_id == pid:
        return product.generate_fluid_data()
      
    return "No product found with requested PID", 400
  else:
    return "Invalid PID", 400
