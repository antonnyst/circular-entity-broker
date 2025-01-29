import requests
import json 

DB_URI = "http://database:7200"
REPO_NAME = "ceb"

PRODUCT_PREFIX = "http://ceb.ltu.se/components/"

def send_sparql_query(sparql_query):
    
    headers = {'Accept': 'application/json', "content-type": "application/x-www-form-urlencoded"}
    
    response = requests.post(DB_URI+"/repositories/"+REPO_NAME, data={'query': sparql_query}, headers=headers)
    
    # Return
    return response

# Retrieves an products properties
def get_properties(product_name):
    query = """ 
        PREFIX cmp: <{PRODUCT_PREFIX}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?property where {{
            ?property rdf:type rdfs:Property ;
                    rdfs:domain cmp:{product} .
        }}
    """.format(product = product_name, PRODUCT_PREFIX=PRODUCT_PREFIX)

    response = send_sparql_query(query)

    # Convert list of lists to just a list
    properties = list(map(lambda x: x[0], sparql_parse(response.text)))
    
    # Remove the product prefix
    properties = list(map(lambda x: x.removeprefix(PRODUCT_PREFIX+product_name+":"), properties))
    
    return properties

# Parses sparql responses into python list of lists
def sparql_parse(raw_json):
    parsed = json.loads(raw_json)

    variables = parsed["head"]["vars"]
    data = parsed["results"]["bindings"]

    list_list = []

    for prop in data:
        row = []
        for variable in variables:
            row.append(prop[variable]["value"])
        list_list.append(row)

    return list_list

# Run som tests if this module was ran independently
if __name__ == "__main__":
    print(get_properties("sawblade"))