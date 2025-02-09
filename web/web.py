from flask import Flask, request, render_template, session
import requests
  

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    #Gets products from broker
    url = "http://broker:5000/components"
    products = requests.get(url).text
    return render_template('index.html', products=products)

@app.route('/resultprod', methods=['GET', 'POST'])
def resprod():
    #Sends product to broker and gets properties for that product
    product = request.args.get('product')
    url = f"http://broker:5000/properties?product={product}"
    properties = requests.get(url)
    properties = properties.json()

    #Storing it in session, which means we can access it from any function
    session['product'] = product
    session['properties'] = properties
    return 'ok'

@app.route('/search', methods=['GET', 'POST'])
def search():
    url = "http://broker:5000/components"
    products = requests.get(url).text
    product = session.get('product')
    properties = session.get('properties')

    return render_template('properties.html',  products=products, properties=properties, product=product)

def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

@app.route('/resultprop', methods=['POST'])
def resprop():
    session['compare'] = []
    #Formatting the json request as specified
    data = {
            "limit": 10,
            "offset": 0,
            "query": []
     }
    #Changing query according to the specification for every property
    properties = request.get_json()["data"]
    for key, value in properties.items():
        if check_float(value) and key == "teethAmount":
            usevalue = int(value)
            data["query"].append({"queryType": "exact", "valueType" : "float", "property": key, "value": usevalue})

        elif check_float(value) and key != "id":
            usevalue = float(value)
            data["query"].append({"queryType": "exact", "valueType" : "float", "property": key, "value": usevalue})

        else:
            data["query"].append({"queryType": "exact", "valueType" : "string", "property": key, "value": value})
    session['compare'] = get_compare(data)

    return 'ok'

def get_compare(data):
    headers = {"Content-Type": "application/json"}
    url = "http://broker:5000/query"
    properties = requests.post(url, json=data, headers=headers)
    compare_json = properties.json()
    return compare_json

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    url = "http://broker:5000/components"
    products = requests.get(url).text

    product = session.get('product')
    match = session.get('compare')
    return render_template('match.html',  products=products, product=product, match = match)


if __name__ == '__main__':
    app.run(debug=True, port=80)
