# Initiative Tracker
# By Gabe Williams
# Tutorial Program

from flask import Flask, redirect, render_template, request, url_for
from processing import make_combatant, sort_combatants

app = Flask(__name__)
app.config["DEBUG"] = True

combatants = []

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", combatants=combatants)
    combatants.append(make_combatant(request.form["name"], request.form["modifier"], request.form["roll"]))
    sort_combatants(combatants, True, True)
    return redirect(url_for('index'))
