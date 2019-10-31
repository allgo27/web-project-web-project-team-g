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
            print("while loop for fans triggered")
            if len(book1Fans) > i:
                commonFanSet.add(book1Fans[i])

            if len(book2Fans) > i:
                commonFanSet.add(book2Fans[i])

            i += 1

        if i > 3:
            print("Error: insufficient data for this query")
            return None



        return commonFanSet

    def getBookListIntersections(self, fanSet, book1, book2):


        # Okay so Liz and I majorly reworked this one, but basically it takes the set of fans, and
        # then for each of the first 100 fans (feel free to tweak the number) it adds
        # every book they like to the dictionary bookDict, and every time a second person
        # likes the book we increment its value by 1, so by the end the most well-liked books
        # by this crowd will have the highest values. Then we'll use GetTopBooks to find the books
        # with highest values and return their IDs.
        i = 0
        bookDict = {}
        for userID in fanSet:  # Iterate through fans
            if i > 100:
                break
            # changed userID to userID[0]
            userBooks = self.getBookList(userID[0])
            for book in userBooks:
                if book in bookDict:
                    bookDict[book] += 1
                else:
                    bookDict[book] = 1

            i += 1

        del bookDict[tuple(str(book1))]
        del bookDict[tuple(str(book2))]

        j = 0
        # This while loop suxxxxxxxx meaning that it's supposed to only come up if none of our fans like any
        # books except for the input books, which seems super unlikely. AND YET. It keeps getting triggered,
        # not sure why, and then when we try to getBookList from the randomfan even randomfan doesn't seem to
        # have a book they like. (that's why we're getting index[0] is out of range errors, I think).
        while len(bookDict) < 3 and j < 100:
            randomFan = fanSet.pop()
            randomBookList = self.getBookList(randomFan)
            randomBook = randomBookList[0]
            if randomBook != book1 and randomBook != book2 and not randomBook in bookDict:
                bookDict[randomBook[-1]] = 1
                # This should hopefully add the last book
                # randomFan liked to the dictionary, so it's
                # a semi random (but hopefully still useful) recommendation
            j += 1

        return bookDict

    def getTopBooks(self, bookDict, fanSet):
        # Returns list of top 3 books with highest value (ie number of relevant fans)
        # Finds max value using code modified from thewolf's suggestion on StackExchange
        bookRecList = []
        for i in range(3):
            bookRecList.append(max(bookDict, key=lambda key: bookDict[key]))
            bookDict.pop(bookRecList[i])
        return bookRecList

    def getFans(self, bookID):
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
        # if there are none, what do we do?
        bookDict = self.getBookListIntersections(commonFanSet, bookID1, bookID2)
        topBooks = self.getTopBooks(bookDict, commonFanSet)

        if len(topBooks) == 0:
            print("Error no books for you")
            return None
        else:
            return topBooks


def main():
    data = DataSource()
    data.connect("allgoodm", "cow254happy")
    fanset = data.getFanIntersections(1, 2)
    bookDict = data.getBookListIntersections(fanset, 1, 2)
    # print(bookDict)
    # print(data.getTopBooks(bookDict, fanset))

main()