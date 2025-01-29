import json
from flask import Flask, request, render_template, redirect, url_for, session
app = Flask(__name__)

@app.route('/')
def index():
    #For testing
    products = ['sawblade', 'Cars', 'Computers', 'sawblade']
    return render_template('index.html', products=products)

@app.route('/resprod', methods=['GET', 'POST'])
def resprod():
    #product = request.form.get('data')
    return 'ok'



@app.route('/search', methods=['GET', 'POST'])
def search():
    #For testing
    #products = ['sawblade', 'Cars', 'Computers']
    #properties = ['product', 'id', 'manufacturer', 'teethgrade', 'teethamount']
    return render_template('properties.html', products=products, properties=properties)

@app.route('/resprop', methods=['POST'])
def resprop():
    properties = request.get_json('data')
    #print(properties)
    return 'ok'

def search():
    return 'ok'
if __name__ == '__main__':
    app.run(debug=True, port=80)
