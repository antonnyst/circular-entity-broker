from flask import Flask, request, render_template
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

app = Flask(__name__)

# Initialize RDFLib graph and namespaces
g = Graph()
STIX = Namespace("http://stix.mitre.org/")
EX = Namespace("http://example.org/")

# Load RDF data
g.parse("data.rdf", format="xml")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = perform_search(query)
    return render_template('search_results.html', results=results)

@app.route('/rdf', methods=['POST'])
def rdf_query():
    query = request.form['rdf_query']
    results = perform_sparql_query(query)
    return render_template('rdf_results.html', results=results)

def perform_search(query):
    # Mock function to simulate search results
    return [
        {"title": "APT28 Threat Actor", "url": "http://example.org/threat_actor/apt28"},
        {"title": "Malware Indicator", "url": "http://example.org/indicator/malware"},
        {"title": "Phishing Attack Pattern", "url": "http://example.org/attack_pattern/phishing"}
    ]

def perform_sparql_query(query):
    q = prepareQuery(query)
    formatted_results = []

    # Parse the SPARQL query
    qres = g.query(q)

    # # Iterate over the results
    # for row in qres:
    #     # Convert each item in the row to a string
    #     #formatted_row = tuple(str(item) for item in row)
    #     formatted_results.append(row)
    return qres

if __name__ == '__main__':
    app.run(debug=True)