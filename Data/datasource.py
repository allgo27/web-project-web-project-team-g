import psycopg2
import getpass

class DataSource:
    '''
	DataSource executes all of the queries on the database.
	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
    '''
    
    def __init__(self):
        self.connection = None
        
    def connect(self, user, password):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        Copied from code by Amy Dalal (and used with permission)
        '''
        try:
            self.connection = psycopg2.connect(database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()
            
        return 
    
    def getBookID(self, title, author):
        '''
        Returns the database "book_id" number for specified title by specified author
        PARAMETERS:
            title - the book's title
            author - the book's author
        RETURN:
            Database "book_id" number
        '''
        return ""
    
    
    
    def getGoodreadsBookID(self, title, author):
        '''
        get Goodreads "goodreads_book_id" number based off of bookID
        PARAMETERS:
            bookID - the database ID number for the book
        RETURN:
            Database "goodreads_book_id" number
        '''
        return ""
        
    def getBookRating(self, bookID):
        '''
        Returns tuple of average rating of book and number of people who have rated it overall
        PARAMETERS:
            bookID - the database ID number for the book 
        
        RETURN:
            a tuple of average rating of book and number of people who have rated it overall
        '''
        return ()

    def getBookTags(self, goodreadsBookID):
        '''
        Returns a list of top three tags of given book according to goodreadsBookID
        PARAMETERS:
            goodreadsBookID - the goodreads ID number for the book
        RETURN:
            a tuple of top 3 tags for a given book
        '''
        return ()
        
    def getImageURL(self, bookID):
        '''
        Returns the url of an image of specified book
        PARAMETERS:
            bookID - the database ID number for the book
        RETURN:
            a string containing the URL of an image of the specified book
        '''
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT image_url FROM books WHERE book_id=" + str(bookID)
            cursor.execute(query)
            return cursor.fetchall()
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return
        
    def getAuthor(self, bookID):
        '''
        Returns the author of specified book
        PARAMETERS:
            bookID - the database ID number for the book
        RETURN:
            a string containing the name of the author of the specified book
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT authors FROM books WHERE book_id=" + str(bookID) 
            cursor.execute(query)
            return cursor.fetchall()
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return 
        
    def getTitle(self, bookID):
        '''
        Returns the title of specified book
        PARAMETERS:
            bookID - the database ID number for the book
        RETURN:
            a string containing the name of the specified book
        '''
        try:
            cursor = self.connection.cursor()
            book = str(bookID)
            #query = "SELECT title FROM books WHERE book_id=" + book
            #cursor.execute(query)
            query = "SELECT title FROM books WHERE book_id=(%s);" 
            cursor.execute(query, (str(bookID),))
            return cursor.fetchone()
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
        
    
    def getBookRecommendation(self, bookID1, bookID2):
        '''
        Returns the database bookIDs of three recommended books
        PARAMETERS:
            bookID1 - the first book to base recommendation off of
            bookID2 - the second book to base recommendation off of
            
        RETURN:
        a tuple of three database bookIDs
        '''
        return ()
    
    
def main():
    data = DataSource()
    data.connect("allgoodm", "cow245happy")
    #answer = data.getTitle(1)
    #print(answer[0])
    print(data.getTitle(4))
    #mylist = []
    #mylist.append(data.getTitle(1))
    #mylist.append(data.getAuthor(1))
    #mylist.append(data.getImageURL(1))
    #print(mylist)
    
    
main()
