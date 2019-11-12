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

    def getPossibleAuthors(self, title):
        '''
        returns all possible authors for a given book title
        :param title:
        :return:
        '''
        try:
            cursor = self.connection.cursor()
            title = str(title)
            query = "SELECT authors FROM books WHERE title=(%s);"
            cursor.execute(query, (str(title),))
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
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

    def getBookList(self, userID):
        '''
        Returns a list of book_ids from the ratings file for a particular user.

        PARAMETERS:
            userID - a user ID number for a given user
        RETURN:
            a list of books where each book is a tuple
        '''

        try:
            cursor = self.connection.cursor()
            query = "SELECT book_id FROM ratings WHERE user_id=(%s);"
            cursor.execute(query, (str(userID),))
            return cursor.fetchall()


        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getFanIntersections(self, bookID1, bookID2):
        '''
        Returns a list of user_ids of users who rated bookID1 and bookID2 highly in the ratings file

        PARAMETERS:
            bookID1 - a database ID number for the first input book
            bookID2 - a database ID number for the second input book
        RETURN:
            a list of user_ids
        '''

        book1Fans = self.getFans(bookID1)
        book2Fans = self.getFans(bookID2)
        book1FanSet = set(book1Fans)
        book2FanSet = set(book2Fans)
        commonFanSet = book2FanSet.intersection(book1FanSet)

        '''
        if there are fewer than 3 fans, adds fans of book one to the common fan set.
        if there are still fewer than 3 fans, it adds the fans of book two to the common fan set.
        else, it returns an error stating that there is insufficient data (which will appear as a pop-up
        for our users when we get to that stage)
        '''

        i = 0
        while len(commonFanSet) < 3:
            if len(book1Fans) > i:
                commonFanSet.add(book1Fans[i])

            if len(book2Fans) > i:
                commonFanSet.add(book2Fans[i])

            if i > 1:
                print("Error: insufficient data for this query")
                return None
            i += 1



        return commonFanSet

    def getBookListIntersections(self, fanSet, book1, book2):
        '''
        Returns a dictionary of books with values corresponding to how many users in fanSet rated them highly

        PARAMETERS:
            fanSet - a list of user_ids of users who rated bookID1 and bookID2 highly in the ratings file
            book1 - a database ID number for the first input book
            book2 - a database ID number for the second input book
        RETURN:
            a dictionary of books with values corresponding to how many users in fanSet rated them highly
        '''

        i = 0
        bookDict = {}
        for userID in fanSet:
            if i > 100:
                break

            userBooks = self.getBookList(userID[0])
            for book in userBooks:
                if book in bookDict:
                    bookDict[book] += 1
                else:
                    bookDict[book] = 1

            i += 1
        if book1 in bookDict:
            del bookDict[tuple(str(book1))]
        if book2 in bookDict:
            del bookDict[tuple(str(book2))]

        j = 0


       #If bookDict lacks sufficient books, add one fan's liked books to bookDict until it has enough.
        #pick a fan. If that fan has 3 or more books, choose their books. Else, pick another fan. Repeat.
        booksNeeded = 3 - len(bookDict)
        if booksNeeded > 0:
            while len(fanSet) != 0:
                randomFan = fanSet.pop()
                randomBookList = self.getBookList(randomFan[0])
                if len(randomBookList) >= booksNeeded:
                    for i in range(booksNeeded):
                        randomBook = randomBookList[i]
                        if randomBook != book1 and randomBook != book2:
                            bookDict[randomBookList[i]] = 1
                    break
            if len(bookDict) < 3:
                print("Error: insufficient data. Please try again with new books.")
                #We don't have enough information to generate results; rather than returning None we will figure out how to convey this information to the user
                return None

        return bookDict

    def getTopBooks(self, bookDict):
        # Finds max value using code modified from thewolf's suggestion on StackExchange
        '''
        Returns list of top 3 books with highest value (ie number of relevant fans)

        PARAMETERS:
            bookDict - a dictionary of books with values corresponding to how many users in fanSet rated them highly
            fanSet - a list of user_ids of users who rated bookID1 and bookID2 highly in the ratings file
        RETURN:
            a list of top 3 books with highest value (ie number of relevant fans)
        '''
        bookRecList = []
        for i in range(3):
            bookRecList.append(max(bookDict, key=lambda key: bookDict[key]))
            bookDict.pop(bookRecList[i])
        return bookRecList

    def getFans(self, bookID):
        '''
        Returns a list of user_ids of users who highly rated a particular book

        PARAMETERS:
            bookID - the database ID number for the book
        RETURN:
            a list of user_ids of users who highly rated a particular book
        '''

        cursor = self.connection.cursor()
        query = "SELECT user_id FROM ratings WHERE book_id=(%s);"
        cursor.execute(query, (str(bookID),))

        return cursor.fetchall()

    def getBookRecID(self, bookID1, bookID2):
        '''
        Returns the database bookIDs of three recommended books
        PARAMETERS:
            bookID1 - the first book to base recommendation off of
            bookID2 - the second book to base recommendation off of

        RETURN:
            a tuple of three database bookIDs
        '''
        commonFanSet = self.getFanIntersections(bookID1, bookID2)

        if commonFanSet == None:
            return None
        bookDict = self.getBookListIntersections(commonFanSet, bookID1, bookID2)
        topBooks = self.getTopBooks(bookDict)

        if len(topBooks) == 0:
            print("Error no books for you")
            return None
        else:
            return topBooks
def makeTesterList():
    lst = list()
    dict = {}
    dict['title'] = 'The Huner Games'
    dict['author'] = 'Suzanne Collins'
    dict['optionNum'] = 'option0'
    lst.append(dict)
    return lst

def main():
    db = DataSource()
    db.connect("allgoodm", "cow245happy")
    print(db.getPossibleAuthors("The Hunger Games"))

if __name__ == "__main__":
    main()
    
