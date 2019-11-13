import flask
from flask import render_template
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)
db = DataSource()
#db.connect("yime2", "tablet389cow")
db.connect("bruelle", "spider268awesome")
#db.connect("allgoodm", "cow245happy")

@app.route('/')
def homePage():
    
    return render_template('WRhomepage.html')

#@app.route('/midresults')
#def midresults():
#    return render_template('midresults.html')
    

    
@app.route('/fakehomepage')
def data():
    
    return render_template('fakehomepage.html')

@app.route('/data')
def data():
    
    return render_template('data.html')


@app.route('/fruit')
def fruit():
    myFruit = [
        {'name': 'apple', 'rating': 7, 'bleh': 1},
        {'name': 'pineapple', 'rating': 6, 'bleh': 3},
        {'name': 'guava', 'rating': 2, 'bleh': 8}
    ]

    return render_template('fruit.html',
                           fruits=myFruit)


@app.route('/midresults/', methods=['POST','GET']) #added the methods=... part with Andy
def midresults():
    if request.method == 'POST': #added the 'POST' and if statement. This code is from his flask app that I have in email. We can look at this for help.
    
        result = request.form
        firstbook = result['firstbook']
        secondbook = result['secondbook'] 
        
    #    firstbook = request.args.get('firstbook')
    #    secondbook = request.args.get('secondbook')
        firstBookAuthors = db.getPossibleAuthors(firstbook) #getPossibleAuthors does not work
        secondBookAuthors = db.getPossibleAuthors(secondbook)
        potentialBooks = list ()
        i = 0
        for author in firstBookAuthors:
            optionDict = {}
            optionDict['title'] = firstbook
            optionDict['author'] = author[0] 
            optionDict['optionNum'] = 'option'+str(i)
            potentialBooks.append(optionDict)
            i += 1
            
        for author in secondBookAuthors:
            optionDict = {}
            optionDict['title'] = secondbook
            optionDict['author'] = author[0] #if we're having problems indexing out of range you don't actually need the [0] but I'm pretty sure we do
            optionDict['optionNum'] = 'option'+str(i)
            potentialBooks.append(optionDict)
            i += 1

        potentialBooks = [
            {'title': 'apple', 'author': 'orangutan', 'optionNum':option0},
            {'title': 'banana', 'author': 'jim'},
            {'title': 'pear', 'author': 'terry'}
        ]
        #potentialBooks = makeTesterList()
        return render_template('http://perlman.mathcs.carleton.edu:5103/midresults.html',
                               books=potentialBooks) #changed from potentialBooks to firstBookAuthors but 


def main():
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    


    

if __name__ == '__main__':
    main()
    

