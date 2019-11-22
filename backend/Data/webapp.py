#TODO:
#readDescription? (if takes longer than 10 mins, not worth it)
#review final rubric to make sure we're doing okay 
#add note that says loading rcommendations may take a hot sec but it'll be worth it (can't read everything in three seconds you know)
#add to homepage and newSearch that dataset is from 2017 (but check spellg if pretty sure it should be there)

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


@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        result = request.form
        book1ID = result['book1']
        book2ID = result['book2']
        bookrecs = db.getBookRecID(book1ID, book2ID)
        if bookrecs == None:
            return render_template('insufficientdata.html')
        bookInfoList = list()
        for book in bookrecs:
            newbook = {}
            newbook['title'] = db.getTitle(book[0])[0]
            newbook['author'] = db.getAuthor(book[0])[0]
            newbook['image_url'] = db.getImageURL(book[0])[0]
            newbook['avg_rating'] = db.getBookRating(book[0])[0]
            searchURL = "https://www.amazon.com/s?k="+db.getTitle(book[0])[0]
            newbook['searchURL'] = searchURL
            bookInfoList.append(newbook)
        #edge case: what if we don't have enough info?
    return render_template('results.html', bookList=bookInfoList)

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
            book1ID = db.getBookID(firstbook, author[0])
            print(book1ID)
            optionList.append(db.getTitle(book1ID)[0])
            optionList.append(author[0]) 
            optionList.append(book1ID)
            
            print("option list 1", optionList)
            potentialBook1s.append(optionList)
            
        potentialBook2s = list()
        
        for author in secondBookAuthors:
            optionList = list()
            book2ID = db.getBookID(secondbook, author[0])
            print(book2ID)
            optionList.append(db.getTitle(book2ID)[0])
            optionList.append(author[0]) 
            optionList.append(book2ID)
            print("option list 2", optionList)
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
    

