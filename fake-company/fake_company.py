from flask import Flask, request
import requests, sys
from product import Product
import json

app = Flask(__name__)

# TEMP: Hard-coded config values
COMPANY_NAME = "FakeCompany"
BROKER_URL = "http://localhost:7100"

registered = False

# Load JSON data
products = []
with open("product_data.json", "r") as file:
    data = json.load(file)
    for prod in data:
      products.append(Product(prod["pid"], prod["name"], prod["description"], prod["price"], prod["stock"], prod["creation_date"]))


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

@app.get("/invoke/product_creation")
def invoke_product_creation():
  # count = 0
  # for prod in products:
  #   count += 1
  #   json_data = {"properties": []}
  #   x = requests.post(BROKER_URL + "/product", json = json_data)

  #   print(x.text)

  #   if count > 1: return "Exceeded"
  
  json_data = {"properties": []}
  x = requests.post(BROKER_URL + "/product", json = json_data)
  print(x.status_code)

  return "OK"
    

@app.route("/api/fluid_data")
def update_fluid_data():
  pid = request.args.get("pid", "")
  if pid != "":
    for prod in products:
      if prod.product_id == pid:
        return prod.toJson()
  else:
    return "Invalid PID"
