
# Initiative Tracker Web App
# By Gabe Williams
# GitHub: CodeWizzard201
# MYSQL pass: rAw&xn7U*$gJ@Lt4^SsMNJe33b
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="RedWizard",
    password="rAw&xn7U*$gJ@Lt4^SsMNJe33b",
    hostname="RedWizard.mysql.pythonanywhere-services.com",
    databasename="RedWizard$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
@app.route('/', methods=["GET", "POST"]) # Accepts whichever methods you list, so GET and POST in this case
def index():
    if request.method == "GET":
        return render_template ("index.html")
    return redirect(url_for('index'))

