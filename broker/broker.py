from app import app

from flask import request
import requests
import uuid
import os
import db
from flask_cors import CORS

CORS(app)

@app.route("/")
def main():
    return "Endpoints: /product /abandon /query"

# Genereate productId as a string with the form 
# '9fe2c4e93f654fdbb24c02b15259716c'
def generate_productId():
    return uuid.uuid4().hex




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
    access_token = request.headers.get("X-API-CAT")
    company_id = db.verify_access_token(access_token)
    if company_id is None:
        return "Error verifying access token", 500

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
    result = db.add_product(productId, product_name, product_properties, company_id)
    
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
    product_name = request.json["product_name"]

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

            # For string searches
            case "like":
                prop = db.get_full_property_uri(product_name, query["property"])
                if prop == None:
                    return {
                        "code": 500,
                        "message": "Invalid property"
                    }
                if query["valueType"] != "string" or not validate_value(query["value"], query["valueType"]):
                    return {
                        "code": 500,
                        "message": "Invalid value/valueType"
                    }

                selection_string += """
                    ?product <{prop}> ?like{propName} .
                    filter contains(?like{propName}, \"{value}\")
                """.format(
                    prop=prop,
                    propName=query["property"],
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

# Returns all component(product types) names in database
@app.get("/fluid_properties")
def fluid_properties():
    product_name = request.args.get('product')

    props = db.get_fluid_properties("http://ceb.ltu.se/components/"+product_name, strip_prefix=True)

    parents = db.get_parent_products("http://ceb.ltu.se/components/"+product_name)
    for parent in parents:
        props.extend(db.get_fluid_properties(parent, strip_prefix=True))

    result = []

    for prop in props:
        result.append(
            {
                "property": prop[0],
                "valueType": prop[1]
            }
        )

    return result

@app.get("/interrogate")
def interrogate():
    productId = request.args.get('productId')
    prop = request.args.get('property')

    # Get product name from id
    types = db.get_types_from_product_id(productId)

    # Validate that property is an fluid property
    schema_fluid_properties = []
    
    for t in types:
        schema_fluid_properties.extend(db.get_fluid_properties(t,strip_prefix=True))

    #[
    # [
    #   "price",
    #   "float"
    # ],
    # [
    #   "stock",
    #   "float"
    # ]
    #]

    valid = False
    for schema_prop in schema_fluid_properties:
        if prop == schema_prop[0]:
            valid = True
            break
    
    if not valid:
        return "Invalid properties", 500

    # Get company id from product
    companyId = db.get_company_from_product_id(productId)

    # Get addresses for interrogation
    urls = db.get_company_urls(companyId)
    if urls == None or len(urls) == 0:
        return "Company does not support interrogation", 500
    
    # Interrogate until property is found
    value = None
    debug_string = ""
    for url in urls:
        headers = {'Accept': 'application/json', "content-type": "application/json"}
        data = []
        data.append(productId)
        response = requests.post("http://"+url+"/api/fluid_data", json=data, headers=headers)
        debug_string += response.text
        if response.ok:
            json = response.json()[0]
            for p in json["properties"]:
                if p["property"] == prop:
                    value = p
                    break
            if value != None:
                break

    if value == None:
        return debug_string, 404
    
    # Return this shit
    return value