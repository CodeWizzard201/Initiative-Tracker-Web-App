# Initiative Tracker
# By Gabe Williams
# Tutorial Program

from flask import Flask, redirect, render_template, request, url_for, session
from processing import make_combatant, sort_combatants

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "sdfueoqhwerhkfniperqjfdcnckalsfjfnn"

session_tags = ["name", "mod", "roll"]

@app.route('/', methods=["POST", "GET"])
def index():
    for tag in session_tags:
        if tag not in session:
            session[tag] = []
    print(request.form)
    if "Clear Combatants" in request.form:
        session["name"].clear()
        session["mod"].clear()
        session["roll"].clear()
        session.modified = True

    # errors: Holds error text for the page
    errors = ""
    # descend and tiebreaker: holds the boolean value for the sorting options for the page
    descend = False
    tiebreaker = False
    if request.method == "POST":
        #if request.form["action"] == "Clear Combatants":
            #session["name"].clear()
            #session["mod"].clear()
            #session["roll"].clear()
            #session.modified = True
        #else:
            try:
                if request.form["name"] is None or request.form["modifier"] is None or request.form["roll"] is None:
                    raise Exception("One or more of the values is invalid.")
                session["name"].append(str(request.form["name"]))
                session["mod"].append(int(request.form["modifier"]))
                session["roll"].append(int(request.form["roll"]))
                # So if either of these are unchecked, the form sends nothing, meaning that it will throw an exception because that request.form section is None.
                # This ensures that None value will be skipped over to prevent errors and keeps the setting as False
                if "descend" in request.form:
                    descend = request.form["descend"]
                if "tiebreaker" in request.form:
                    tiebreaker = request.form["tiebreaker"]
                session.modified = True
            except:
                errors += "Invalid inputs, please check your inputs for each section."

    combatants = []

    for name, mod, roll in zip(session["name"], session["mod"], session["roll"]):
        combatants.append(make_combatant(name, mod, roll))

    sort_combatants(combatants, descend, tiebreaker)
    return render_template("index.html", errors=errors, combatants=combatants, descend=descend, tiebreaker=tiebreaker)
