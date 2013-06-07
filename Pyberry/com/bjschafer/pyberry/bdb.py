import sqlite3 as sqlite
class Bdb(object):
    '''
    database for storing the books.  uses python3 builtin module
    sqlite3.  it stores book objects, but it doesn't pickle
    or serialize them or anything awful like that.  it just
    stores each aspect of the object in the db as a separate
    column.  the bc is the primary key.
    '''


    def __init__(self, location):
        '''
        creates the connection to the database, currently
        an example file.  i should change that but i don't feel
        like it at the moment.  it also creates the table/schema
        if it doesn't exist.
        '''
        self.fields = ["bc", "isbn", "title", "authors", "pages", "publ_year",
                       "publisher", "location", "description", "call_num", "tags"]
        self.conn = sqlite.connect(location)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS books
        (bc INTEGER PRIMARY KEY,
        isbn INTEGER,
        title TEXT,
        authors TEXT,
        pages INTEGER,
        publ_year INTEGER(4),
        publisher TEXT,
        location TEXT,
        description TEXT,
        call_num TEXT,
        tags TEXT)''') # not sure how the tags will store.  they're an array and although they
        # should go in there correctly, there's no telling how they'll come out.  i'll have
        # to check it out.
        self.conn.commit()
        c.close()
                
    def store(self, book):
        '''
        stores the book object in the database.  again, it
        doesn't serialize it or do anything awful like that.
        '''
        c = self.conn.cursor()
        t = book.getListRepresentation()
        t[-1] = str(t[-1])
        t = tuple(t)
        c.execute('''INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',t)
        self.conn.commit()
        c.close()
        
    def delete(self, book):
        '''
        Deletes a book in the database.  This will require
        some testing to ensure I've gotten it right.
        '''

        c = self.conn.cursor()
        c.execute('''DELETE FROM books WHERE bc=?''', (book.bc,))
        self.conn.commit()
            
    def retrieve(self, bc):
        '''
        retrieves a book given the barcode/unique id.
        '''
        c = self.conn.cursor()
        c.execute('''SELECT * FROM books WHERE bc=?''', bc)
        return c.fetchone()
    
    def search(self, field, term):
        '''Searches for records given the field to search and
        the term to search for.
        
        I couldn't say what might happen if an invalid field is
        given.  So I'll add error checking.
        '''
        if field not in self.fields:
            return -1
        
        else:
            term = '%' + term + '%'

            c = self.conn.cursor()
            
            # @attention: I know using format for parameters isn't technically
            # safe or secure.  I did it for two reasons.  Number one, it just
            # wouldn't work with pysqlite placeholders.  Number two, because
            # I have it fail above if the field isn't in a predefined list of
            # fields, it /should/ be okay.
            c.execute('''SELECT * FROM books WHERE {} LIKE ?'''.format(field),(term,))
            return c.fetchall()
        
    def getAll(self):
        '''
        Returns a list of all items in the database.
        '''
        c = self.conn.cursor()
        c.execute('''SELECT * FROM books''')
        return c.fetchall()        