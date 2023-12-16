
# A very simple Flask Hello World app for you to get started with...

from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

