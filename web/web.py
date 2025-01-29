import json
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
    # For An array of JSON for testing
    properties = []
    properties.append(json.dumps({"product" : "Sawblade", "id" : "", "manufacturer": "", "teethgrade":"", "teethamount":""}))
    properties.append(json.dumps({"product" : "Cars", "id" : "", "manufacturer": "", "plåtkvalite":"", "Hjul":""}))
    properties.append(json.dumps({"product" : "Sawblade", "id" : "", "manufacturer": "", "teethGrade":"", "teethamount":""}))
    return render_template('index.html', properties=properties)
@app.route('/results', methods=['POST'])
def results():
    output = request.get_json()
    res = json.loads(output)
    print(res)
    return res


#This will not be fixed but one website each company who have the specification
@app.route('/Biltema')
def manufacturer():
    return "It works"

def search():
    return 'ok'
if __name__ == '__main__':
    app.run(debug=True, port=80)