import requests

DB_URI = "http://database:7200"
REPO_NAME = "ceb"

def send_sparql_query(sparql_query):
    
    headers = {'Accept': 'application/json', "content-type": "application/x-www-form-urlencoded"}
    
    response = requests.post(DB_URI+"/repositories/"+REPO_NAME, data={'query': sparql_query}, headers=headers)
    
    # Return
    return response.content
