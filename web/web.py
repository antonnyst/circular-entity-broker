import json
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
    # For An array of JSON for testing
    properties = []
    properties.append(json.dumps({"product" : "Sawblade", "id" : "1", "manufacturer": "Biltema", "teethGrade":"1.5", "teethamount":"65"}))
    properties.append(json.dumps({"product" : "Cars", "id" : "2", "manufacturer": "Toyota", "plåtkvalite":"5", "Hjul":"4"}))
    properties.append(json.dumps({"product" : "Sawblade", "id" : "3", "manufacturer": "Kebert", "teethGrade":"7", "teethamount":"90"}))
    return render_template('index.html', properties=properties)
@app.route('/search', methods=['POST'])

#This will not be fixed but one website each company who have the specification
@app.route('/Biltema')
def manufacturer():
    return "It works"

def search():
    return 'ok'
if __name__ == '__main__':
    app.run(debug=True, port=7300)