'''
Created on Nov 30, 2012

@author: braxton
'''
import sqlite3 as sqlite

class Bdb(object):
    '''
    database for storing the books.  uses python3 builtin module
    sqlite3.  it stores book objects, but it doesn't pickle
    or serialize them or anything awful like that.  it just
    stores each aspect of the object in the db as a separate
    column.  the bc is the primary key.

    @todo implement searching of database
    '''


    def __init__(self, location):
        '''creates the connection to the database, currently
        an example file.  i should change that but i don't feel
        like it at the moment.  it also creates the table/schema
        if it doesn't exist.'''
        self.conn = sqlite.connect(location)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS books
        (bc INTEGER PRIMARY KEY,
        isbn INTEGER,
        title TEXT,
        author TEXT,
        pages INTEGER,
        publ_year INTEGER(4),
        publisher TEXT,
        location TEXT,
        description TEXT,
        call_num TEXT,
        tags TEXT)''') # not sure how the tags will store.  they're an array and although they
        #should go in there correctly, there's no telling how they'll come out.  i'll have
        #to check it out.
        self.conn.commit()
        c.close()
                
    def store(self, book):
        '''stores the book object in the database.  again, it
        doesn't serialize it or do anything awful like that.'''
        c = self.conn.cursor()
        for t in book.getListRepresentation(): # not sure if this is the right way to do it.
            c.execute('''INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',t)
        self.conn.commit()
        c.close()
            
    def retrieve(self, bc):
        '''retrieves a book given the barcode/unique id.'''
        c = self.conn.cursor()
        c.execute('''SELECT * FROM books WHERE bc=?''', bc)
        return c.fetchone()
        