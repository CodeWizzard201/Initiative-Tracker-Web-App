# Initiative Tracker
# By Gabe Williams
# Tutorial Program

from flask import Flask, render_template
from processing import Combatant, make_combatant

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return render_template("index.html")
