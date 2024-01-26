# Initiative Tracker
# By Gabe Williams

from flask import Flask, redirect, render_template, request, url_for, session
from processing import Combatant, make_combatant, sort_combatants

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "sdfueoqhwerhkfniperqjfdcnckalsfjfnn"

session_tags = ["combatants", "descend", "tiebreaker"]

@app.route('/', methods=["POST", "GET"])
def index():
    for tag in session_tags:
        if tag not in session:
            session[tag] = []

    # errors: Holds error text for the page
    errors = ""
    if request.method == "POST":
        try:
            print(request.form["name"])
            print(request.form["modifier"])
            print(request.form["roll"])
            if request.form["name"] is None or request.form["modifier"] is None or request.form["roll"] is None:
                print("Raised")
                raise Exception("One or more of the values is invalid.")

            new_combatant = make_combatant(str(request.form["name"]), int(request.form["modifier"]), int(request.form["roll"]))
            print(new_combatant)
            session["combatants"].append(new_combatant.to_json())

            session["descend"] = request.form.get("descend",False)
            session["tiebreaker"] = request.form.get("tiebreaker", False)

            session.modified = True
        except:
            print("Except Triggered")
            errors += "Invalid inputs, please check your inputs for each section."

    combatants = session.get("combatants", [])

    #Converts from JSON to the original Combatant object for sorting
    original_combatants = [Combatant(**combatant_data) for combatant_data in combatants]

    #Sort by the specified parameters
    sort_combatants(original_combatants, session.get("descend", False), session.get("tiebreaker", False))

    #Converts back to json and the json combatant list
    combatants = [combatant.to_json() for combatant in original_combatants]

    return render_template("index.html", errors=errors, combatants=combatants, descend=session.get("descend",False), tiebreaker=session.get("tiebreaker", False))

#@app.route('/delete/<uuid>', method == ["POST"])
#def delete(uuid):
     # Find the index of the combatant to delete using its UUID
    #index_to_delete = None
    #for i, combatant_data in enumerate(combatants):
       # if combatant_data['id'] == uuid:
           # index_to_delete = i
           # break

   # if index_to_delete is not None:
      #  del combatants[index_to_delete]  # Delete the combatant from the list
       # session['combatants'] = combatants  # Update the session

    # Redirect to the main page or display a confirmation message
  #  return redirect(url_for('index'))  # Example of redirection