from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from db_caller import get_query

app = Flask(__name__)
CORS(app)

@app.route("/", methods=('GET', 'POST'))
def what_up():
    # return "What up"
    results = []
    print(request.form)
    if len(request.form) > 0:
        term = request.form['term']
        # results = get_results("tad_pantherID", term)
        results = get_query("gene2enhancers", {"gene": term})
        # return str(request.form)
    return render_template("search.html", results=results, result_count=len(results))

@app.route("/search/<gene>")
def search(gene):
    results = get_query("gene2enhancers", {"gene": gene})
    return jsonify(results)

#### Startup on remote server:
#### FLASK_APP=server.py flask run -h 0.0.0.0