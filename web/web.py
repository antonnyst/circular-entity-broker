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
    i = 0
    product_name = session.get('product')
    #Formatting the json request as specified
    data = {
            "product_name": product_name,
            "limit": 10,
            "offset": 0,
            "query": []
     }
    #Changing query according to the specification for every property
    properties = request.get_json()["data"]
    valueType = request.get_json()["valueType"]
    for key, value in properties.items():
            queryType = valueType[i] == "string" and "like" or "exact"
            data["query"].append({"queryType": queryType, "valueType" : valueType[i], "property": key, "value": value})
            i += 1
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
    properties = session.get('properties')
    product = session.get('product')
    match = session.get('compare')
    return render_template('match.html',  products=products, product=product, match = match, properties=properties)


if __name__ == '__main__':
    app.run(debug=True, port=80)