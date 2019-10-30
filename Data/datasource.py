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
            book = str(bookID)
            query = "SELECT image_url FROM books WHERE book_id=(%s);"
            cursor.execute(query, (str(bookID),))
            return cursor.fetchone()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
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
            book = str(bookID)
            query = "SELECT authors FROM books WHERE book_id=(%s);"
            cursor.execute(query, (str(bookID),))
            return cursor.fetchone()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
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
            query = "SELECT title FROM books WHERE book_id=(%s);"
            cursor.execute(query, (str(bookID),))
            return cursor.fetchone()


        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getFanIntersections(self, bookID1, bookID2):
        # Return intersection of fans of both books
        book1Fans = set(self.getFans(bookID1))
        book2Fans = set(self.getFans(bookID2))
        commonFans = book2Fans.intersection(book1Fans)
        print(book1Fans)
        print(book2Fans)
        i = 0
        while len(commonFans) < 3:
            if len(book1Fans) > i:
                commonFans.add(book1Fans[i])

            if len(book2Fans) > i:
                commonFans.add(book2Fans[i])

            if i > 3:
                print("Error: insufficient data for this query")
                return None

            i+=1

        return commonFans[0:2]

    def getBookList(self, userID):
        try:
            cursor = self.connection.cursor()
            query = "SELECT book_id FROM ratings WHERE user_id=(%s);"
            cursor.execute(query, (str(userID),))
            return cursor.fetchall()


        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getBookListIntersections(self, userID1, userID2):
        # Return intersection of fans of both books
        user1Books = set(self.getBookList(userID1))
        user2Books = set(self.getBookList(userID2))
        commonBooks = user1Books.intersection(user2Books)

        return commonBooks

    def getFans(self, bookID):
        try:
            cursor = self.connection.cursor()
            query = "SELECT user_id FROM ratings WHERE book_id=(%s);"
            cursor.execute(query, (str(bookID),))
            return cursor.fetchall()


        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getBookRecID(self, bookID1, bookID2):
        '''
        Returns the database bookIDs of three recommended books
        PARAMETERS:
            bookID1 - the first book to base recommendation off of
            bookID2 - the second book to base recommendation off of

        RETURN:
        a tuple of three database bookIDs
        '''
        commonFans = self.getFanIntersections(bookID1, bookID2)
        #if there are none, what do we do?
        commonBooks = self.getBookListIntersection(commonFans[0], commonFans[1])
        #if there are none, what do we dooooo?
        if len(commonBooks) > 3:
            commonBooks = commonBooks[0:4]
        if len(commonBooks) == 0:
            print("Error no books for you")
            return None
        else:
            return commonBooks


def main():
    data = DataSource()
    data.connect("bruelle", "spider268awesome")
    bookTitle = data.getTitle(4)
    author = data.getAuthor(4)
    image = data.getImageURL(4)
    mylist = []
    mylist.append(bookTitle[0])
    mylist.append(author[0])
    mylist.append(image[0])
    #print(mylist)
    #print(data.getFanIntersections(5, 10000))
    #print(data.getBookList(7747))
    #print(data.getBookListIntersections(7747, 7717))


main()