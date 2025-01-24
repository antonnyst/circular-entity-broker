from flask import Flask
from flask import request
import requests
import uuid
import db

app = Flask(__name__)

@app.route("/")
def main():
    return "Endpoints: /product /abandon /query"

# Genereate productId as a string with the form 
# '9fe2c4e93f654fdbb24c02b15259716c'
def generate_productId():
    return uuid.uuid4().hex

# Create new product
# NOTE does not check and validate valueType coming from request
# since rdf schema does not define types for the parameters'
# https://www.w3.org/TR/2013/REC-sparql11-update-20130321/
@app.post("/product")
def product_post():
    print(request.json)
    
    product_name = "sawblade" # Assuming sawblade until API supports specifying product name
    
    # Convert to (uri, value)
    product_properties = list(
        map(lambda prop: 
            (prop["property"], prop["value"]), 
            request.json["properties"]
        )
    )

    # Validate  properties into rdf triples
    schema_properties = db.get_properties("http://ceb.ltu.se/components/sawblade", strip_prefix=True)

    parents = db.get_parent_products("http://ceb.ltu.se/components/sawblade")
    for parent in parents:
        schema_properties.extend(db.get_properties(parent, strip_prefix=True))

    properties = []
    for prop in product_properties:
        if prop[0] not in schema_properties:
            # They sent an property which is not in our schema
            return {
                "code": 500,
                "message": "Invalid property in properties" + prop[0]
            }
        else:
            properties.append(prop)

    # Generate productId
    productId = generate_productId()


    # Send query to db
    result = db.add_product(productId, product_name, properties)
    
    if not result.ok:
        return {
            "code": 500,
            "message": "Error adding product"
        }


    # Return OK with productID and properties.
    return {
        "productId": productId,
        "properties": product_properties
    }

# Modify product
@app.put("/product")
def product_put():
    # TODO
    return "OK"

# Remove product
@app.delete("/product")
def product_delete():
    # TODO
    return "OK"

@app.post("/abandon") 
def abandon():
    # TODO
    return "OK"

@app.post("/query")
def query():
    # Get query
    sparql_query = request.form['query']
    
    # Check authentication?
    # TODO

    # Send to DB
    headers = {'Accept': 'application/json', "content-type": "application/x-www-form-urlencoded"}
    
    response = requests.post(DB_URI+"/repositories/"+REPO_NAME, data={'query': sparql_query}, headers=headers)
    
    # Return
    return response.content


if __name__ == '__main__':
    app.run(debug=True, port=7100)