from flask import Flask
from flask import request
import requests
import db

app = Flask(__name__)

@app.route("/")
def main():
    return "Endpoints: /register /unregister /abandon /query"

@app.post("/unregister")
def unregister():
    # TODO
    return "OK"

@app.post("/register")
def register():
    # Maybe file upload
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