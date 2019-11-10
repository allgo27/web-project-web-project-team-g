import flask
from flask import render_template
import json
import sys

app = flask.Flask(__name__)


@app.route('/midresults')
def books():
    potentialBooks = [
        {'title': 'apple', 'author': 'orangutan'},
        {'title': 'banana', 'author': 'jim'},
        {'title': 'pear', 'author': 'terry'}
    ]

    return render_template('midresults.html',
                           books=potentialBooks)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)

    