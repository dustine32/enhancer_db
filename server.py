from flask import Flask, render_template, request
from db_caller import get_results

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def what_up():
    # return "What up"
    results = []
    print(request.form)
    if len(request.form) > 0:
        term = request.form['term']
        results = get_results("tad_pantherID", term)
        # return str(request.form)
    return render_template("search.html", results=results)
