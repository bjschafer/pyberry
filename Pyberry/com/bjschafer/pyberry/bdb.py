import sqlite3 as sqlite


class Bdb(object):
    """
    database for storing the books.  uses python builtin module
    sqlite3.  it stores book objects, but it doesn't pickle
    or serialize them or anything awful like that.  it just
    stores each aspect of the object in the db as a separate
    column.  the bc is the primary key.
    """

    def __init__(self, location):
        """
        Create connection to database and table/schema.

        @type location: basestring
        @param location: the file location of the database
        """

        self.book_fields = ["bc", "isbn", "title", "authors", "pages", "publ_year",
                            "publisher", "location", "description", "call_num", "tags"]
        self.person_fields = ["id", "first_name", "last_name", "email", "phone_num", "address", "city", "state", "notes"]

        assert isinstance(location, basestring)
        self.conn = sqlite.connect(location)
        self.conn.text_factory = str
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
        tags TEXT)''')  # not sure how the tags will store.  they're an array and although they
        # should go in there correctly, there's no telling how they'll come out.  i'll have
        # to check it out.

        c.execute('''CREATE TABLE IF NOT EXISTS people
        (id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone_num TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        notes TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS loans
        (id INTEGER PRIMARY KEY,
        book INTEGER,
        person INTEGER,
        issue_date TEXT,
        due_date TEXT,
        is_historical INTEGER(1))''')

        self.conn.commit()
        c.close()

    def store_book(self, book):
        """
        Store the given book object in the database.

        @param book: the book object to store

        It doesn't serialize or do anything awful like that.
        """

        c = self.conn.cursor()
        t = book.get_list_representation()
        t[-1] = str(t[-1])  # what do these lines do? # wow, talk about bad programming/commenting
        t[3] = str(t[3])
        if t[0] == -1 or t[0] == '-1':  # if the barcode is -1, e.g. should autoincrement
            del t[0]
            t = tuple(t)
            c.execute('''INSERT OR REPLACE INTO books (isbn, title, authors, pages, publ_year, publisher, location,
                         description, call_num, tags)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', t)
        else:
            t = tuple(t)
            c.execute('''INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', t)
        self.conn.commit()
        c.close()

    def delete_book(self, book):
        """
        Delete a book in the database
        @param book: book object to delete
        """

        c = self.conn.cursor()
        c.execute('''DELETE FROM books WHERE bc=?''', (book.bc,))
        self.conn.commit()

    def retrieve_book(self, bc):
        """
        Retrieve a book given barcode/unique id.
        @param bc: the book's barcode to fetch
        @return: the book requested
        """

        c = self.conn.cursor()
        c.execute('''SELECT * FROM books WHERE bc=?''', (bc,))
        return c.fetchone()

    def search_book(self, field, term):
        """
        Search for records given field to search and term to search for.

        @param field: the field to search in (e.g title, author)
        @param term: the term to search for
        @return: all matching results

        Field checking is implemented here to be sure - we have a list of known fields, and before any query is
        executed, it's checked against the valid fields.  This is especially important because we use string formatting
        to insert the field.
        """

        if field not in self.book_fields:
            return -1

        else:
            term = '%' + term + '%'

            c = self.conn.cursor()

            # @attention: I know using format for parameters isn't technically
            # safe or secure.  I did it for two reasons.  Number one, it just
            # wouldn't work with sqlite3 placeholders.  Number two, because
            # I have it fail above if the field isn't in a predefined list of
            # fields, it /should/ be okay.
            c.execute('''SELECT * FROM books WHERE {} LIKE ?'''.format(field), (term,))
            return c.fetchall()

    def get_all_books(self):
        """
        Fetch a list of all items in the database.

        @return: raw unadulterated DB goodness
        """

        c = self.conn.cursor()
        c.execute('''SELECT * FROM books''')
        return c.fetchall()

    def store_person(self, person):
        c = self.conn.cursor()
        t = person.get_list_representation()

        if t[0] == -1 or t[0] == '-1':
            del t[0]
            t = tuple(t)
            c.execute('''INSERT OR REPLACE INTO people (first_name, last_name, email, phone_num, address, city, state, notes)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', t)
        else:
            t = tuple(t)
            c.execute('''INSERT OR REPLACE INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', t)

        self.conn.commit()
        c.close()

    def retrieve_person(self, uid):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM people WHERE id=?''', (uid,))
        return c.fetchone()

    def search_person(self, field, term):
        if field not in self.person_fields:
            return -1

        else:
            term = '%' + term + '%'

            c = self.conn.cursor()

            c.execute('''SELECT * FROM people WHERE {} LIKE ?'''.format(field),(term,))
            return c.fetchall()

    def store_loan(self, loan):
        c = self.conn.cursor()
        l = loan.get_list_representation()

        l[1] = l[1].bc
        l[2] = l[2].uid
        l[-1] = 0 if True else 1 # for some reason this needs to be backwards...

        if l[0] == -1 or l[0] == '-1':
            del l[0]
            l = tuple(l)
            c.execute('''INSERT OR REPLACE INTO loans (book, person, issue_date, due_date, is_historical) VALUES (?, ?, ?, ?, ?)''', l)
        else:
            l = tuple(l)
            c.execute('''INSERT OR REPLACE INTO loans VALUES (?, ?, ?, ?, ?, ?)''', l)

        self.conn.commit()
        c.close()

    def get_all_loans(self):
        c = self.conn.cursor()
        c.execute('''SELECT loans.id, books.title, people.first_name, people.last_name FROM loans
                     JOIN books ON loans.book=books.bc
                     JOIN people on loans.person=people.id
                     WHERE loans.is_historical=0''')
        return c.fetchall()