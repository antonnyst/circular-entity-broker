from flask import Flask, request, render_template
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
from pathlib import Path

app = Flask(__name__)

# Initialize RDFLib graph and namespaces
g = Graph()
STIX = Namespace("http://stix.mitre.org/")
EX = Namespace("http://example.org/")

# Load RDF data


pathlist = Path("../rdf").glob('**/*.ttl')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)   
    print(path_in_str)
    g.parse(path_in_str, format="turtle")
    g.print()
    # print(path_in_str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = perform_sparql_query(query)
    return render_template('search_results.html', results=results)

@app.route('/rdf', methods=['POST'])
def rdf_query():
    query = request.form['rdf_query']
    results = perform_sparql_query(query)
    return render_template('rdf_results.html', results=results)

def perform_sparql_query(query):
    q = prepareQuery(query)
    formatted_results = []

    # Parse the SPARQL query
    qres = g.query(q)

    
    # # Iterate over the results
    
        
    #     formatted_results.append(row)
    return qres

if __name__ == '__main__':
    app.run(debug=True)