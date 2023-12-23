# Initiative Tracker
# By Gabe Williams
# Tutorial Program

from flask import Flask, redirect, render_template, request, url_for, session
from processing import make_combatant, sort_combatants

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "sdfueoqhwerhkfniperqjfdcnckalsfjfnn"

session_tags = ["name", "mod", "roll", "descend", "tiebreaker"]

@app.route('/', methods=["POST", "GET"])
def index():
    for tag in session_tags:
        if tag == "descend" or tag == "tiebreaker":
            session[tag] = True

        elif tag not in session:
            session[tag] = []

    errors = ""
    if request.method == "POST":
        try:
            session["name"].append(str(request.form["name"]))
            session["mod"].append(int(request.form["modifier"]))
            session["roll"].append(int(request.form["roll"]))
            session.modified = True
        except:
            errors += "Invalid inputs, please check your inputs for each section."

    combatants = []

    for name, mod, roll in zip(session["name"], session["mod"], session["roll"]):
        combatants.append(make_combatant(name, mod, roll))

    sort_combatants(combatants, session["descend"], session["tiebreaker"])
    return render_template("index.html", errors=errors, combatants=combatants)
