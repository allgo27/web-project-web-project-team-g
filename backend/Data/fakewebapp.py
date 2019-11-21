import flask
from flask import render_template
from flask import *
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



@app.route('/data')
def data():
    
    return render_template('data.html')


@app.route('/newsearch',)

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
#       if len(firstBookAuthors) == 0:
#            return render_template('newsearch.html', book=firstbook)
#        
#        if len(secondBookAuthors) == 0:
#            return render_template('newsearch.html', book=secondbook)
        
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
            optionDict['author'] = author[0] 
            optionDict['optionNum'] = 'option'+str(i)
            potentialBooks.append(optionDict)
            i += 1

            
        return render_template('midresults.html',
                               books=potentialBooks) 


def main():
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
    


    

if __name__ == '__main__':
    main()
    

