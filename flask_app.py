# Initiative Tracker
# By Gabe Williams

from flask import Flask, render_template, request, session, jsonify
from processing import Combatant, make_combatant, sort_combatants
from secret import config_settings

app = Flask(__name__)
app = config_settings(app)

session_tags = ["combatants", "descend", "tiebreaker"]

@app.route('/', methods=["GET"])
def index():
    for tag in session_tags:
        if tag not in session:
            session[tag] = []

    combatants = session.get("combatants", [])

    #Converts from JSON to the original Combatant object for sorting
    original_combatants = [Combatant(**combatant_data) for combatant_data in combatants]

    #Sort by the specified parameters
    sort_combatants(original_combatants, session.get("descend", False), session.get("tiebreaker", False))

    #Converts back to json and the json combatant list
    combatants = [combatant.to_json() for combatant in original_combatants]

    return render_template("index.html", combatants=combatants, descend=session.get("descend",False), tiebreaker=session.get("tiebreaker", False))

@app.route('/get_combatant/<string:combatant_id>', methods=['GET'])
def get_combatant(combatant_id):
    for combatant in session["combatants"]:
        if combatant['id'] == combatant_id:
            combatant_data = combatant
            break

    if not combatant_data:
        return jsonify({'error': 'Combatant not found'}), 400

    return jsonify(combatant_data)

@app.route('/create_combatant', methods = ['POST'])
def create_combatant():
    #errors: Holds error text for the page
    errors = ""
    try:
        name = request.form.get("name")
        modifier = request.form.get("modifier")
        roll = request.form.get("roll")

        if not all([name, modifier, roll]):
            raise Exception("One or more of the values is invalid.")

        new_combatant = make_combatant(name, modifier, roll)
        session["combatants"].append(new_combatant.to_json())
        session["descend"] = request.form.get("descend",False)
        session["tiebreaker"] = request.form.get("tiebreaker", False)

        session.modified = True
        return jsonify({"success": True})
    except Exception as e:
        errors = str(e)
        return jsonify({"success": False, "error": errors})

@app.route('/update_combatant', methods = ["PUT"])
def update_combatant():
    combatant_id = request.json.get("id")
    for combatant in session["combatants"]:
        if combatant['id'] == combatant_id:
            old_combatant = combatant
            combatant['name'] = request.json.get("name")
            combatant['mod'] = request.json.get("mod")
            combatant['roll'] = request.json.get("roll")

            # Delete the old combatant
            session['combatants'].remove(old_combatant)

            # Add the new version to the list
            session['combatants'].append(combatant)

            session.modified = True
            break
    if not session.modified:
        return jsonify({'error': 'Combatant not found'}), 400

    return jsonify({'success': 'Combatant updated'})

@app.route('/delete_combatant', methods = ["POST"])
def delete_combatant():
    combatant_id = request.json.get("combatantID")
    combatant_to_remove = None
    for combatant in session["combatants"]:
        if combatant['id'] == combatant_id:
            combatant_to_remove = combatant
            break

    if combatant_to_remove:
        session['combatants'].remove(combatant_to_remove)
        session.modified = True
        return jsonify({"success": True})

    else:
        return jsonify({"success": False, "error": "Invalid Combatant ID"}), 400