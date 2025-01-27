from flask import Flask, request
from product import Product
import json

app = Flask(__name__)

# Load JSON data
products = []
with open("product_data.json", "r") as file:
    data = json.load(file)
    for prod in data:
      products.append(Product(prod["pid"], prod["name"], prod["description"], prod["price"], prod["stock"], prod["creation_date"]))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
  
@app.route("/invoke")
def invoke_registration():
  # Invoke a registration with the broker. This should only be used once after startup
  pass

@app.route("/product")
def get_product_data():
  pid = request.args.get("pid", "")
  if pid != "":
    for prod in products:
      if prod.product_id == pid:
        return prod.toJson()
  else:
    return "Invalid PID"  

@app.route("/product-multiple")
def get_multiple_data():
  pass

