import unittest
import psycopg2
from datasource import *


class MyTestCase(unittest.TestCase):
    def test_basic(self):
        ds = DataSource()
        ds.connect("allgoodm", "cow254happy")
        booklist = ds.getBookRecID(1,2)
        self.assertEqual(len(booklist), 3)

    def test_few_fans(self):
       ds = DataSource()
       ds.connect("allgoodm", "cow254happy")
       booklist = ds.getBookRecID('hp7', 'lightning')
       self.assertEqual(len(booklist), 3)

    def test_no_common_books(self):
       ds = DataSource()
       ds.connect("allgoodm", "cow254happy")
       booklist = ds.getBookRecID(10001, 30000)
       self.assertEqual(booklist, None)

if __name__ == '__main__':
    unittest.main()
