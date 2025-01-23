from flask import Flask
from flask import request
import requests

DB_URI = "http://database:7200"
REPO_NAME = "ceb"

app = Flask(__name__)

@app.route("/")
def main():
    return "Endpoints: /product /abandon /query"

# Create new product
@app.post("/product")
def product_post():
    # TODO
    return "OK"

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