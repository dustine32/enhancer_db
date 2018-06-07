from flask import Flask, render_template, request
from db_caller import get_query

app = Flask(__name__)

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
