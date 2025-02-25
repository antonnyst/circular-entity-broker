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
    query = """ 
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select * where {
            ?s rdfs:subClassOf <http://ceb.ltu.se/broker/product> .
            FILTER (?s != <http://ceb.ltu.se/broker/product>)
        }
    """


    pass

@app.post("/interrogation")
def company_interrogation_post():
    url = request.json["url"]
    
    access_token = request.headers.get("X-API-CAT")

    company_id = db.verify_access_token(access_token)

    result = db.add_company_url(company_id, url)

    return "OK"

@app.delete("/interrogation")
def company_interrogation_delete():
    pass