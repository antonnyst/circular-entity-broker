from app import app
from flask import request
import uuid
import os

import db
# For all the company endpoint lovers! 🥰💅


def generate_companyId():
    return uuid.uuid4().hex

def generate_accessToken():
    return os.urandom(64).hex()


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

@app.get("/interrogation")
def company_interrogation_get():
    access_token = request.headers.get("X-API-CAT")

    query = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX broker: <http://ceb.ltu.se/broker/>
        PREFIX cmp: <http://ceb.ltu.se/components/>
        PREFIX data: <http://ceb.ltu.se/data/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?url WHERE {{
            ?company broker:company:accessToken "{token}"^^xsd:string ;
                broker:company:interrogation_url ?url .
        }}
    """.format(token=access_token)

    response = db.send_sparql_query(query)
    if not response.ok:
        return [], 500
    
    result = db.sparql_parse(response.text)
    
    result = list(map(lambda x: x[0], result))

    return result

@app.post("/interrogation")
def company_interrogation_post():
    url = request.json["url"]
    
    access_token = request.headers.get("X-API-CAT")

    company_id = db.verify_access_token(access_token)

    if company_id is None:
        return "Error verifying access token", 500

    result = db.add_company_url(company_id, url)

    return "OK"

@app.delete("/interrogation")
def company_interrogation_delete():
    url = request.args.get("url")
    
    access_token = request.headers.get("X-API-CAT")

    company_id = db.verify_access_token(access_token)

    if company_id is None:
        return "Error verifying access token", 500

    result = db.remove_company_url(company_id, url)

    if not result.ok:
        return "Error", 500
    
    return "OK"