from flask import Flask
from flask import request
import requests
import uuid
import os
import db

app = Flask(__name__)

@app.route("/")
def main():
    return "Endpoints: /product /abandon /query"

# Genereate productId as a string with the form 
# '9fe2c4e93f654fdbb24c02b15259716c'
def generate_productId():
    return uuid.uuid4().hex

def generate_companyId():
    return uuid.uuid4().hex

def generate_accessToken():
    return os.urandom(64).hex()


def validate_valuetype(valueType):
    match valueType:
        case "string":
            return True
        case "float":
            return True
        case _:
            return False

# Makes sure the value is an propert valueType (and that the valueType is proper)
def validate_value(value, valueType):
    if not validate_valuetype(valueType):
        return False
    
    match valueType:
        case "string":
            return True # Anything can be a string (i guess)
        case "float":
            try:
                float(value)
                return True
            except ValueError:
                return False

# Create new product
# NOTE does not check and validate valueType coming from request
# since rdf schema does not define types for the parameters'
# https://www.w3.org/TR/2013/REC-sparql11-update-20130321/
@app.post("/product")
def product_post():    
    product_name = "sawblade" # Assuming sawblade until API supports specifying product name
    
    # Convert to (uri, value)
    product_properties = list(
        map(lambda prop: 
            (prop["property"], prop["value"], prop["valueType"]), 
            request.json["properties"]
        )
    )
    
    #Get schema properties
    validateProps(product_name, product_properties)

    # Generate productId
    productId = generate_productId()

    # Send query to db
    result = db.add_product(productId, product_name, product_properties)
    
    if not result.ok:
        return {
            "code": 500,
            "message": "Error adding product"
        }

    # Return OK with productID and properties.
    return {
        "productId": productId,
        "properties": request.json["properties"]
    }


def validateProps(product_name, product_properties):
    # Get schema properties
    schema_properties = list(map(lambda x: x[0], db.get_properties("http://ceb.ltu.se/components/"+product_name, strip_prefix=True)))

    parents = db.get_parent_products("http://ceb.ltu.se/components/"+product_name)
    for parent in parents:
        schema_properties.extend(
            list(map(lambda x: x[0], db.get_properties(parent, strip_prefix=True)))
        )

    # Validate properties against schema
    for prop in product_properties:
        if prop[0] not in schema_properties:
            # They sent an property which is not in our schema
            return False
        elif not validate_value(prop[1], prop[2]):
            return False
    
    return True
            
        

# Modify product
@app.put("/product")
def product_put():

    product_name = "sawblade" #remove later
    
    productId = request.args.get("productId")

    product_properties = list(
        map(lambda prop: 
            (prop["property"], prop["value"], prop["valueType"]), 
            request.json["properties"]
        )
    )

    validateProps(productId, product_properties)


    result1 = db.delete_product(productId)
    if not result1.ok: 
        return {
            "code": 500,
            "message": "Error removing old data",
            "why?": result1.text #Vital, if removed API breaks
        }
         
    
    result2 = db.add_product(productId, product_name, product_properties)
    if not result2.ok: 
        return {
            "code": 500,
            "message": "Error adding new data",
            "why": result2.text #Vital, if removed API breaks
        }
    else: 
        return {
            "code": 200,
            "message": "Ok"
        }


# Remove product
@app.delete("/product")
def product_delete():
    
    #get product ID
    productId = request.args.get("productId")

    #Delete productID
    result = db.delete_product(productId)

    #Error handling 
    if not result.ok: 
        return {
            "code": 500,
            "message": "Error deleting product",
            "why?": result.text #Vital, if removed API breaks
        }

    #This is what we like to see (We see it a lot)
    return {
        "code": 200,
        "message": "OK"
    } 

@app.post("/abandon") 
def abandon():
    # TODO
    return "OK"

@app.post("/query")
def query():
    product_name = "sawblade" # Assuming sawblade until API supports specifying product name

    schema_properties = list(
        map(
            lambda x: x[0], db.get_properties(
                "http://ceb.ltu.se/components/"+product_name, strip_prefix=True
            )
        )
    )

    parents = db.get_parent_products("http://ceb.ltu.se/components/"+product_name)
    for parent in parents:
        schema_properties.extend(
            list(map(lambda x: x[0], db.get_properties(parent, strip_prefix=True)))
        )

    property_count = len(schema_properties);
    
    limit = request.json["limit"] * property_count; # I loooove typecasting
    offset = request.json["offset"]
    propertyQueries = request.json["query"]

    if len(propertyQueries) == 0:
        return {
            "code": 500,
            "message": "Invalid properties"
        } 

    selection_string = ""

    for query in propertyQueries:
        match query["queryType"]:
            case "exact":
                prop = db.get_full_property_uri(product_name, query["property"])
                if prop == None:
                    return {
                        "code": 500,
                        "message": "Invalid property"
                    }
                if not validate_value(query["value"], query["valueType"]):
                    return {
                        "code": 500,
                        "message": "Invalid value/valueType"
                    }

                selection_string += "?product <{prop}> \"{value}\"^^xsd:{type} .".format(
                    prop=prop,
                    value=query["value"],
                    type=query["valueType"]
                )
            case _:
                return {
                    "code": 500,
                    "message": "Invalid queryType"
                }

    query = """ 
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        select ?product ?properties ?values ?datatype where {{
            # product selection
            {selection_string}

            # just works?!
            ?product rdf:type ?types .
            ?properties rdfs:domain ?types .
            ?product ?properties ?values .
            ?properties rdfs:range ?datatype .
        }} LIMIT {limit} OFFSET {offset}
    """.format(selection_string=selection_string, limit=limit, offset=offset)

    # Check authentication?
    # TODO

    # Send to DB
    response = db.sparql_parse(db.send_sparql_query(query).content)

    # Convert to correft format
    result_dict = {}

    for val in response:
        product_id = val[0].split("/")[-1]
        if not product_id in result_dict:
            result_dict[product_id] = { 
                "productId": product_id,
                "properties": []
            }

        result_dict[product_id]["properties"].append({
            "valueType": val[3].split("#")[-1],
            "property": val[1].split(":")[-1],
            "value": val[2],
        })

    result = []

    for val in result_dict:
        result.append(result_dict[val])

    # Return
    return result

# Returns all properties of an product type
@app.get("/properties")
def properties():
    product_name = request.args.get('product')

    props = db.get_properties("http://ceb.ltu.se/components/"+product_name, strip_prefix=True)

    parents = db.get_parent_products("http://ceb.ltu.se/components/"+product_name)
    for parent in parents:
        props.extend(db.get_properties(parent, strip_prefix=True))

    result = []

    for prop in props:
        result.append(
            {
                "property": prop[0],
                "valueType": prop[1]
            }
        )

    return result

# Returns all component(product types) names in database
@app.get("/components")
def components():
    query = """ 
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select * where {
            ?s rdfs:subClassOf <http://ceb.ltu.se/broker/product> .
            FILTER (?s != <http://ceb.ltu.se/broker/product>)
        }
    """

    response = db.sparql_parse(db.send_sparql_query(query).text)
    
    result = []
    
    for res in response:
        result.append(res[0].split("/")[-1])

    return result

# Register a new company and send back access token
@app.post("/register")
def company_register():
    company_name = request.json["name"]
    
    companyId = generate_companyId();

    accessToken = generate_accessToken();

    company_properties = [
        ["name", company_name, "string"],
        ["accessToken", accessToken, "string"]
    ] 

    db.add_company(companyId, company_properties);

    return {
        "companyId": companyId,
        "accessToken": accessToken
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
