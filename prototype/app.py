from flask import Flask, request, render_template
from rdflib import Graph, Literal, Namespace
from rdflib.plugins.sparql import prepareQuery
from pathlib import Path
import pprint

app = Flask(__name__)

# Initialize RDFLib graph and namespaces
g = Graph()
STIX = Namespace("http://stix.mitre.org/")
EX = Namespace("http://example.org/")

# Load RDF data
results = []
pathlist = Path("../rdf").glob('**/*.ttl')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    g.parse(path_in_str, format="turtle")
    query = '''
        SELECT ?name ?id ?manu ?teethGrade ?teethAmount WHERE {
            ?instance rdf:type cmp:sawblade .
            ?instance product:name ?name .
            ?instance product:id ?id .
            ?instance product:manufacturer ?manu .
            ?instance cmp:sawblade:teethGrade ?teethGrade .
            ?instance cmp:sawblade:teethAmount ?teethAmount .
        }
    '''
    result = g.query(query)
    results.append(result)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    for row in result:
        if Form == row:
            return render_template('rdf_results.html', results=result)

@app.route('/rdf', methods=['POST'])
def rdf_query():
    Form = request.form['rdf_query']
    desc = []
    for instance in results:
        for inst in instance:
            print(inst)
            name = str(inst['name'])
            if Form.__eq__(name):
                id = str(inst['id'])
                manu = str(inst['manu'])
                teethgrade = str(inst['teethGrade'])
                teethamount = str(inst['teethAmount'])
                desc.append(name)
                desc.append(id)
                desc.append(manu)
                desc.append(teethgrade)
                desc.append(teethamount)
        return render_template('rdf_results.html', results=desc)

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