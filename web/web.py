from flask import Flask, request, render_template
from rdflib import Graph, Literal, Namespace
from rdflib.plugins.sparql import prepareQuery
from pathlib import Path

app = Flask(__name__)

# Initialize RDFLib graph and namespaces
g = Graph()
STIX = Namespace("http://stix.mitre.org/")
EX = Namespace("http://example.org/")

# Load RDF data



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    results = perform_sparql_query()
    Form = request.form['query']
    desc = []
    for instance in results:
        for inst in instance:
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
        return render_template('search.html', results=desc)

def perform_sparql_query():
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
    return results

if __name__ == '__main__':
    app.run(debug=True)