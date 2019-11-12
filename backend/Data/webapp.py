import flask
from flask import render_template
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)
#we added this from datasource because maybe you can merge things or maybe we're frankensteining?
db = DataSource()
db.connect("yime2", "tablet389cow")

@app.route('/')
def homePage():
    
    return render_template('WRhomepage.html')
    

@app.route('/midresults/', methods=['POST','GET']) #added the methods=... part with Andy
def midresultsBooks():
<<<<<<< HEAD
    firstBook = request.args.get('firstbook')
    secondBook = request.args.get('secondbook')
    firstPossible = getPossibleBooks(firstBook)
    secondPossible = getPossibleBooks(secondBook)

    
    potentialBooks = [
        {'title': 'apple', 'author': 'orangutan', 'optionNum':i},
        {'title': 'banana', 'author': 'jim'},
        {'title': 'pear', 'author': 'terry'}
    ]
=======
    if request.method == 'POST': #added the 'POST' and if statement. This code is from his flask app that I have in email. We can look at this for help.
    
        result = request.form
        firstbook = result['firstbook']
        secondbook = result['secondbook']
    #    firstbook = request.args.get('firstbook')
    #    secondbook = request.args.get('secondbook')
        firstBookAuthors = db.getPossibleAuthors(firstbook) #getPossibleAuthors does not work
    #    secondBookAuthors = db.getPossibleAuthors(secondbook)
    #    potentialBooks = list ()
    #    i = 0
    #    for author in firstBookAuthors:
    #        optionDict = {}
    #        optionDict['title'] = firstbook
    #        optionDict['author'] = author[0] #if we're having problems indexing out of range you don't actually need the [0] but I'm pretty sure we do
    #        optionDict['optionNum'] = 'option'+str(i)
    #        potentialBooks.append(optionDict)
    #        i += 1
    #        
    #    for author in secondBookAuthors:
    #        optionDict = {}
    #        optionDict['title'] = secondbook
    #        optionDict['author'] = author[0] #if we're having problems indexing out of range you don't actually need the [0] but I'm pretty sure we do
    #        optionDict['optionNum'] = 'option'+str(i)
    #        potentialBooks.append(optionDict)
    #        i += 1
>>>>>>> f81a9a17d10e5a75a11a6550c01cb6dd9dafd535


<<<<<<< HEAD
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
=======
    #    potentialBooks = [
    #        {'title': 'apple', 'author': 'orangutan', 'optionNum':option0},
    #        {'title': 'banana', 'author': 'jim'},
    #        {'title': 'pear', 'author': 'terry'}
    #    ]

        return render_template('midresults.html',
                               books=potentialBooks) #changed from potentialBooks to firstBookAuthors but 


def main():
>>>>>>> f81a9a17d10e5a75a11a6550c01cb6dd9dafd535
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    

<<<<<<< HEAD
    

if __name__ == '__main__':
    main()
    
=======
if __name__ == '__main__':
    main()
>>>>>>> f81a9a17d10e5a75a11a6550c01cb6dd9dafd535
