from flask import Flask, request
import requests, random
from company import FakeCompany

app = Flask(__name__)
# TEMP: Hard-coded config values
BROKER_URL = "http://localhost:7100"
company = FakeCompany()
print("Created FakeCompany with name", company.name)

## API Endpoints (for internal control only, not meant to be a public API):
# GET   /invoke/register - register fake_company with the broker, returns access token
# GET   /invoke/unregister - delete all products and request fake_company to be removed from the broker
# GET   /invoke/set_interrogation - register the company api url with the broker for interrogation
# GET   /invoke/unset_interrogation - unregister the company api url from the broker
# GET   /invoke/create?amount=X - generate X amount of new products (returns copies of the new products as json)
# GET   /invoke/update?amount=X - change the description of X amount of random products
# GET   /invoke/remove?amount=X - delete X amount of random products
# GET   /products - get all products currently belonging to fake_company
#
# GET   /invoke/setup - shorthand to register, set_interrogation and create 3 products
# 
# GET   /api/fluid_data?pid=X - get fluid data (stock/price) for product with product id = X

@app.get("/")
def hello_world():
  return f"<h1>{company.name}</h1>"

@app.get("/invoke/register")
def invoke_registration():
  # Invoke a registration with the broker. This should only be used once after startup
  if company.registered:
    return "Already registered", 400
  
  # Send request to broker
  json = {"name": company.name}
  headers = {'Accept': 'application/json', "Content-type": "application/json"}    
  response = requests.post(BROKER_URL + "/register", json=json, headers=headers)
  data = response.json()
  access_token = data["accessToken"]
  company_id = data["companyId"]
  print("Registered, access token:", access_token)

  if response.status_code == 200:
    company.access_token = access_token
    company.id = company_id
    company.registered = True

  return access_token

@app.get("/invoke/unregister")
def invoke_unregistration():
  # Invoke an unregistration with the broker. This will remove all company data and products from the broker
  if not company.registered:
    return "Not registered", 400
  
  # Send request to broker
  headers = {"X-API-CAT": company.access_token}
  response = requests.delete(BROKER_URL + "/register", headers=headers)

  # TODO: Not implemented in broker
  # if response.status_code == 200:
  #   return "Unregistered"
  # else:
  #   return "Unregistration failed: " + response.text, 500

  return "Unregistration not yet implemented :/"


@app.get("/invoke/set_interrogation")
def invoke_set_url():
  # Set a URL with the broker, this must be the url for the broker to reach fake_company
  if not company.registered:
    return "Not registered", 400
  
  # Send request to broker
  json = {"url": request.host}
  headers = {'Accept': 'application/json', "Content-type": "application/json", "X-API-CAT": company.access_token}    
  response = requests.post(BROKER_URL + "/interrogation", json=json, headers=headers)

  if response.status_code == 200:
    return "Registration successful"

  return "Registration failed: " + response.text, 500

@app.get("/invoke/unset_interrogation")
def invoke_unset_url():
  # Unset a URL from the broker
  if not company.registered:
    return "Not registered", 400
  
  # Send request to broker
  json = {"url": request.host}
  headers = {'Accept': 'application/json', "Content-type": "application/json", "X-API-CAT": company.access_token}    
  response = requests.delete(BROKER_URL + "/interrogation", json=json, headers=headers)

  if response.status_code == 200:
    return "Unregistration successful"

  return "Unregistration failed: " + response.text, 500


# Invoke fake_company to create X amount of new randomized products
@app.get("/invoke/create")
def invoke_product_creation():
  if not company.registered:
    return "Not registered", 400
  
  new_products = company.generateProducts(int(request.args.get("amount")))
  company.products.extend(new_products)
  new_product_jsons = []
  for product in new_products:
    json = {"properties": product.toProperties()}
    headers = {"X-API-CAT": company.access_token}
    response = requests.post(BROKER_URL + "/product", json=json, headers=headers)
    if response.status_code != 200:
      return "Product creation failed", 500
    product.product_id = response.json()["productId"]
    new_product_jsons.append(product.toObject())

  return new_product_jsons

# Invoke fake_company to update X amount of random products
@app.get("/invoke/update")
def invoke_product_update():
  if not company.registered:
    return "Not registered", 400
  
  updated_products = company.updateProducts(int(request.args.get("amount")))
  updated_product_jsons = []
  for product in updated_products:
    json = {"properties": product.toProperties()}
    headers = {"X-API-CAT": company.access_token}
    response = requests.put(BROKER_URL + "/product?productId=" + product.id, json=json, headers=headers)
    if response.status_code != 200:
      return "Product update failed", 500
    updated_product_jsons.append(product.toObject())

  return updated_product_jsons

# Invoke fake_company to remove X amount of random products
@app.get("/invoke/remove")
def invoke_product_remove():
  if not company.registered:
    return "Not registered", 400
  
  removed_products = company.removeProducts(int(request.args.get("amount")))
  removed_product_jsons = []
  for product in removed_products:
    headers = {"X-API-CAT": company.access_token}
    response = requests.delete(BROKER_URL + "/product?productId=" + product.id, headers=headers)
    if response.status_code != 200:
      return "Product deletion failed", 500
    removed_product_jsons.append(product.toObject())

  return removed_product_jsons


# Invoke fake_company to register, set URL and create 3 products
@app.get("/invoke/setup")
def invoke_setup():
  # Invoke a registration with the broker. This should only be used once after startup
  if company.registered:
    return "Already registered", 400

  print("Setting up company...")
  
  # Send request to broker
  json = {"name": company.name}
  headers = {'Accept': 'application/json', "Content-type": "application/json"}    
  response = requests.post(BROKER_URL + "/register", json=json, headers=headers)
  data = response.json()
  access_token = data["accessToken"]
  company_id = data["companyId"]
  print("Registered, access token:", access_token)

  if response.status_code == 200:
    company.access_token = access_token
    company.id = company_id
    company.registered = True
  else:
    return "Failed to register", 500
  
  # Set a URL with the broker, this must be the url for the broker to reach fake_company
  # Send request to broker
  json = {"url": request.host}
  headers = {'Accept': 'application/json', "Content-type": "application/json", "X-API-CAT": company.access_token}    
  response = requests.post(BROKER_URL + "/interrogation", json=json, headers=headers)

  if response.status_code != 200:
    return "Failed to set URL", 500
  
  print("Successfully registered URL", json.get("url"))
  
  new_products = company.generateProducts(3)
  company.products.extend(new_products)
  new_product_jsons = []
  for product in new_products:
    print("Generating product...")
    json = {"properties": product.toProperties()}
    headers = {"X-API-CAT": company.access_token}
    response = requests.post(BROKER_URL + "/product", json=json, headers=headers)
    if response.status_code != 200:
      return "Product creation failed", 500
    print("Product generation succeeded")
    product.product_id = response.json()["productId"]
    new_product_jsons.append(product.toObject())
  
  print("Setup successful")
  return "Setup succeeded"

# Return all stored products (mainly for debug purposes)
@app.get("/products")
def all_products():
  products = []
  for product in company.products:
    products.append(product.toObject())
  return products


# Serve fluid data to the broker
@app.post("/api/fluid_data")
def fluid_data():
  fluid_data = []
  # Get product ids from body
  pids = request.get_json()

  if type(pids) is list:
    # Find product and return its fluid data
    for id in pids:
      found_match = False
      for product in company.products:
        if product.product_id == id:
          fluid_data.append({
            "productId": product.product_id,
            "properties": product.generate_fluid_data(),
          })
          found_match = True
          break

      if not found_match:
        return "ID '" + id + "' does not match any products", 400
      
    return fluid_data
  else:
    return "Invalid PID array", 400

if __name__ == '__main__':
  # Generate a random port
  port = random.randrange(5000, 6000)
  app.run(host="0.0.0.0", port=port, debug=True)
