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
    firstBook = request.args.get('firstbook')
    secondBook = request.args.get('secondbook')
    firstPossible = getPossibleBooks(firstBook)
    secondPossible = getPossibleBooks(secondBook)

    
    potentialBooks = [
        {'title': 'apple', 'author': 'orangutan', 'optionNum':i},
        {'title': 'banana', 'author': 'jim'},
        {'title': 'pear', 'author': 'terry'}
    ]

    return render_template('midresults.html',
                           books=potentialBooks)

#Taken from Amy's slack as an example
@app.route('/resultletter', methods = ['POST', 'GET'])
def resultLetter():
    if request.method == 'POST':
        result = request.form
        ds = datasource.DataSource()
        description = "Showing all names beginning with " + result.get("Letter") + " sorted alphabetically"
        result = ds.getLetter(result.get("Letter"))
        return render_template('result.html', result = result, description = description)

def main:
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    

    

if __name__ == '__main__':
    main()
    
