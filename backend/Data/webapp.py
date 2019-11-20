import flask
from flask import render_template
from flask import *
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)
db = DataSource()
db.connect("yime2", "tablet389cow")
#db.connect("bruelle", "spider268awesome")
#db.connect("allgoodm", "cow245happy")

@app.route('/')
def homePage():
    
    return render_template('WRhomepage.html')



@app.route('/data')
def data():
    
    return render_template('data.html')

#@app.route('/results', methods=['POST','GET']) #maybe get rid of get?
#def results():
    #we hope we're getting fed an optionNum and we also need to somehow have access to our list of dictionaries????? to decipher what 'optionNum' means OH no we should just redo that so optionnum is the bookIDand then we odn't need to pass possibleBooks which would be scary and hard and also we'll need the bookID eventually anyway

@app.route('/midresults', methods=['POST','GET']) 
def midresults():
    if request.method == 'POST': 
    
        result = request.form
        firstbook = result['firstbook']
        secondbook = result['secondbook'] 
        
        firstBookAuthors = db.getPossibleAuthors(firstbook) 
        secondBookAuthors = db.getPossibleAuthors(secondbook)
#       Currently the site crashes when we enter a book not in the database. The following is our general plan for 
#       what to do in this case, but it's not currently functional. 
        if firstBookAuthors == None:
            print("no first book if triggered")
            return render_template('newsearch.html', book=firstbook)

        if secondBookAuthors == None:
            return render_template('newsearch.html', book=secondbook)
        
        potentialBook1s = list()
        
        for author in firstBookAuthors:
            optionList = list()
            optionList[0] = firstbook
            optionList[1] = author[0] 
            optionList[2] = db.getBookID(firstbook, author[0])
            print(optionList)
            potentialBook1s.append(optionList)
            
        potentialBook2s = list()
        
        for author in secondBookAuthors:
            optionList = list()
            optionList[0] = secondbook
            optionList[1] = author[0] 
            optionList[2] = db.getBookID(secondbook, author[0])
            print(optionList)
            potentialBook2s.append(optionList)


            
        return render_template('midresults.html',
                               book1s=potentialBook1s, book2s=potentialBook2s) 


def main():
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    


    

if __name__ == '__main__':
    main()
    

