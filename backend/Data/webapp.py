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
            searchURL = "https://www.betterworldbooks.com/search/results?q="+db.getTitle(book[0])[0]
            newbook['searchURL'] = searchURL
            bookInfoList.append(newbook)
  
    return render_template('results.html', bookList=bookInfoList)

@app.route('/data')
def data():
    
    return render_template('data.html')

@app.route('/midresults', methods=['POST','GET']) 
def midresults():
    if request.method == 'POST': 
        result = request.form
        firstbook = result['firstbook']
        secondbook = result['secondbook'] 
        firstBookAuthors = db.getPossibleAuthors(firstbook) 
        secondBookAuthors = db.getPossibleAuthors(secondbook)
        
        if firstBookAuthors == None:
            print("no first book if triggered")
            return render_template('newsearch.html', book=firstbook)

        if secondBookAuthors == None:
            return render_template('newsearch.html', book=secondbook)
        
        potentialBook1s = list()
        
        for author in firstBookAuthors:
            optionList = list()
            book1ID = db.getBookID(firstbook, author[0])
            optionList.append(db.getTitle(book1ID)[0])
            optionList.append(author[0]) 
            optionList.append(book1ID)
            potentialBook1s.append(optionList)
            
        potentialBook2s = list()
        
        for author in secondBookAuthors:
            optionList = list()
            book2ID = db.getBookID(secondbook, author[0])
            optionList.append(db.getTitle(book2ID)[0])
            optionList.append(author[0]) 
            optionList.append(book2ID)
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
    

