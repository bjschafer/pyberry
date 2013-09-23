class Book(object):
    '''
    classdocs
    '''

    def __init__(self, bc, isbn=0, title="", authors=[], pages=0, publ_year=0, publisher="", location="", description="", call_num="", tags=[]):
        '''
        Constructor
        '''
        self.bc = bc
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.pages = pages
        self.publ_year = publ_year
        self.publisher = publisher
        self.location = location
        self.description = description
        self.call_num = call_num
        self.tags = tags
        
    def edit(self, bc=None, isbn=None, title=None, authors=None, pages=None, publ_year=None, publisher=None, location=None, description=None, call_num=None, tags=None):
        '''Edit a book.  Specify any parameter.  I love Python.'''
        if bc != None:
            self.bc = bc
        if isbn != None:
            self.isbn = isbn
        if title != None:
            self.title = title
        if authors != None:
            self.authors = authors
        if pages != None:
            self.pages = pages
        if publ_year != None:
            self.publ_year = publ_year
        if publisher != None:
            self.publisher = publisher
        if location != None:
            self.location = location
        if description != None:
            self.description = description
        if call_num != None:
            self.call_num = call_num
        if tags != None:
            self.tags = tags
        
    def getListRepresentation(self):
        '''gets a representation of all elements of the book
        in a list, for easy storing in the db.'''
        return [self.bc, self.isbn, self.title, self.authors, self.pages, self.publ_year,
                self.publisher, self.location, self.description, self.call_num, self.tags]
    
    def createFromList(self, myList):
        '''Fills in the details of a book from a list.'''
        if len(myList) != 11:
            raise ValueError("Incorrect list length")
        else:
            self.bc = myList[0]
            self.isbn = myList[1]
            self.title = myList[2]
            self.authors = myList[3]
            self.pages = myList[4]
            self.publ_year = myList[5]
            self.publisher = myList[6]
            self.location = myList[7]
            self.description = myList[8]
            self.call_num = myList[9]
            self.tags = myList[10]
            
    def removeUnicode(self):
        '''
        Removes the unicode (converts it to ascii) from each element of a book.
        Thus, eliminates the obnoxious u'.
        Probably should come up with a better way to deal with unicode someday.
        '''
        
        self.title = self.title.encode('ascii')
        self.authors = self.authors.encode('ascii')
        self.publisher = self.publisher.encode('ascii')
        self.location = self.location.encode('ascii')
        self.description = self.description.encode('ascii')
        self.call_num = self.call_num.encode('ascii')
        
        