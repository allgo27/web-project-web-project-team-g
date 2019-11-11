import flask
from flask import render_template
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)
#we added this from datasource because maybe you can merge things or maybe we're frankensteining?
db = DataSource()
db.connect("allgoodm", "cow245happy")

@app.route('/')
def homePage():
    
    return render_template('WRhomepage.html')


@app.route('/midresults')
def midresultsBooks():
    firstbook = request.args.get('firstbook')
    secondbook = request.args.get('secondbook')
    potentialBooks = [
        {'title': 'apple', 'author': 'orangutan', 'optionNum':i},
        {'title': 'banana', 'author': 'jim'},
        {'title': 'pear', 'author': 'terry'}
    ]

    return render_template('midresults.html',
                           books=potentialBooks)


def main:
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    