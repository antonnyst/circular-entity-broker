from flask import Flask, request
import requests, sys
from product import Product
import json

app = Flask(__name__)

# TEMP: Hard-coded config values
COMPANY_NAME = "FakeCompany"
BROKER_URL = "http://localhost:7100"

registered = False

# TODO:
# - Registration (unimplemented on the broker for now)
# - Product creation based on predefined list
# - Company deletion (unimplemented on broker)
# - Product interrogation with random values
# - Product randomization/generation

# Load JSON data
products = []
with open("product_data.json", "r") as file:
    data = json.load(file)
    for prod in data:
      products.append(Product(prod["pid"], prod["name"], prod["description"], prod["price"], prod["stock"], prod["creation_date"], COMPANY_NAME))


@app.route("/")
def hello_world():
    return f"<h1>{COMPANY_NAME}</h1>"
  
@app.get("/invoke/registration")
def invoke_registration():
  # Invoke a registration with the broker. This should only be used once after startup
  if registered:
    return "Already registered", 400
  
  json_data = {"name": COMPANY_NAME}
  x = requests.post(BROKER_URL + "/register", json = json_data)

  print(x.text)

  # TODO: Not yet implemented in broker

  return "OK"

# Invoke fake_company to create all products from json in the broker
@app.get("/invoke/product_creation")
def invoke_product_creation():
  product_ids = []
  for prod in products:
    json_data = {"properties": prod.toProperties()}
    x = requests.post(BROKER_URL + "/product", json = json_data)
    product_ids.append(x.json()["productId"])

  return product_ids
    

@app.route("/api/fluid_data")
def update_fluid_data():
  pid = request.args.get("pid", "")
  if pid != "":
    for prod in products:
      if prod.product_id == pid:
        return prod.toJson()
  else:
    return "Invalid PID"
