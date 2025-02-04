import requests
import json 

DB_URI = "http://database:7200"
REPO_NAME = "ceb"

BROKER_PREFIX = "http://ceb.ltu.se/broker/"
COMPONENT_PREFIX = "http://ceb.ltu.se/components/"
DATA_PREFIX = "http://ceb.ltu.se/data/"

def send_sparql_query(sparql_query):
    headers = {'Accept': 'application/json', "content-type": "application/x-www-form-urlencoded"}
    response = requests.post(DB_URI+"/repositories/"+REPO_NAME, data={'query': sparql_query}, headers=headers)
    return response

def send_sparql_update(sparql_update):
    headers = {'Accept': 'application/json', "content-type": "application/x-www-form-urlencoded"}    
    response = requests.post(DB_URI+"/repositories/"+REPO_NAME+"/statements", data={'update': sparql_update}, headers=headers)
    return response

# add_product
# product_id : string
# product_name: string
# properties : [(property,value,type),(property2, value2, type2)]
# property assumed just name with no prefix
# product_name assumed to be in cmp prefix
def add_product(product_id, product_name, properties): 
    property_string = ""
    
    for i in range(0,len(properties)):
        print(properties[i])
        prop = properties[i]
        prop_name = get_full_property_uri(product_name, prop[0])
        prop_value = prop[1]
        prop_type = prop[2]
        property_string += " <{}> \"{}\"^^xsd:{} ".format(prop_name, prop_value, prop_type)
        if i < len(properties)-1:
            property_string += ";"
        else:
            property_string += "."
    
    
    query = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX cmp: <{COMPONENT_PREFIX}>
        PREFIX data: <{DATA_PREFIX}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        INSERT DATA {{
            data:{product_id} a cmp:{product} ;
            {property_string}
        }}
    """.format(
        product = product_name,
        product_id=product_id,
        property_string=property_string,
        COMPONENT_PREFIX=COMPONENT_PREFIX,
        DATA_PREFIX=DATA_PREFIX
    )
    
    response = send_sparql_update(query)

    if not response.ok:
        print("Error in add_product")

    return response

def modify_product():
    # TODO
    return

def delete_product():
    # TODO
    return

# Retrieves an products properties based upon its full uri
def get_properties(product_uri, strip_prefix=False):
    #print(product_uri)
    query = """ 
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?property where {{
            ?property rdf:type rdf:Property ;
                    rdfs:domain <{product}> .
        }}
    """.format(product = product_uri)

    #print(query)

    response = send_sparql_query(query)

    # Convert list of lists to just a list
    properties = list(map(lambda x: x[0], sparql_parse(response.text)))
    
    # Remove the product prefix
    if strip_prefix:
        properties = list(map(lambda x: x.split(":")[-1], properties))
    
    return properties

# get_parent_products
# product_uri : full uri string
# returns full uri
def get_parent_products(product_uri):
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?parent where {{
            <{product}> rdfs:subClassOf ?parent .
            
            FILTER(<{product}> != ?parent)
        }}
    """.format(product = product_uri)
    #print(query)
    response = send_sparql_query(query)

    parents = list(map(lambda x: x[0], sparql_parse(response.text)))

    return parents

# get_full_property_uri
# Based upon an product_name (assumed to be in cmp prefix) and an property name finds 
# the namespace the property is in, looking from the specified product and its parents
# product_name : string
# property : string
# returns string or None if not found
def get_full_property_uri(product_name, prop, prefix=COMPONENT_PREFIX):
    # First check properties of specified products
    properties = get_properties(prefix + product_name, strip_prefix=True)
    if prop in properties:
        # We found the property full uri should be
        return prefix + product_name + ":" + prop

    # Then check properties of parent products
    parents = get_parent_products(prefix + product_name)
    for parent in parents:
        properties = get_properties(parent, strip_prefix=True)
        if prop in properties:
            return parent + ":" + prop

    return None

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
    #print(get_full_property_uri("sawblade","manufacturer"))

    add_product("f1a2","sawblade",
        [
            ("name","DetUltimataSågbladet"),
            ("manufacturer","Weyland-Yutani"),
            ("teethGrade", "200"),
            ("teethAmount", "20")
        ]
    )
    print("")