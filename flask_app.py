
# Initiative Tracker Web App
# By Gabe Williams
# GitHub: CodeWizzard201

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
comments = []
app.config["DEBUG"] = True

@app.route('/', methods=["GET", "POST"]) # Accepts whichever methods you list, so GET and POST in this case
def index():
    if request.method == "GET":
        return render_template ("index.html", comments=comments)

    comments.append(request.form["contents"])# Extracts the text from the form given the name from the HTML
    return redirect(url_for('index'))

