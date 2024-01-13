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
        if tag not in session:
            session[tag] = []

    # errors: Holds error text for the page
    errors = ""
    if request.method == "POST":
        try:
            if request.form["name"] is None or request.form["modifier"] is None or request.form["roll"] is None:
                raise Exception("One or more of the values is invalid.")
            session["name"].append(str(request.form["name"]))
            session["mod"].append(int(request.form["modifier"]))
            session["roll"].append(int(request.form["roll"]))
            session["descend"] = request.form.get("descend",False)
            session["tiebreaker"] = request.form.get("tiebreaker", False)
            session.modified = True
        except:
            errors += "Invalid inputs, please check your inputs for each section."

    combatants = []

    for name, mod, roll in zip(session["name"], session["mod"], session["roll"]):
        combatants.append(make_combatant(name, mod, roll))

        sort_combatants(combatants, session.get("descend",False), session.get("tiebreaker", False))
        json_combatants = [combatant.to_json() for combatant in combatants]
        session["combatants"] = json_combatants #Stores the current list of combatants
    sort_combatants(combatants, session.get("descend", False), session.get("tiebreaker", False))
    return render_template("index.html", errors=errors, combatants=combatants, descend=session.get("descend",False), tiebreaker=session.get("tiebreaker", False))

@app.route('/delete', method == ["POST", "GET"])
def delete():
