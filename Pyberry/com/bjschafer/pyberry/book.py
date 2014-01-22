import unicodedata


class Book(object):

    def __init__(self, bc, isbn=0, title="", authors=[], pages=0, publ_year=0, publisher="", location="", description="", call_num="", tags=[]):
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
        if bc is not None:
            self.bc = bc
        if isbn is not None:
            self.isbn = isbn
        if title is not None:
            self.title = title
        if authors is not None:
            self.authors = authors
        if pages is not None:
            self.pages = pages
        if publ_year is not None:
            self.publ_year = publ_year
        if publisher is not None:
            self.publisher = publisher
        if location is not None:
            self.location = location
        if description is not None:
            self.description = description
        if call_num is not None:
            self.call_num = call_num
        if tags is not None:
            self.tags = tags
        
    def get_list_representation(self):
        """
        Get a list representation of book elements for storing in DB.

        @return: This represented as a list.
        """

        return [self.bc, self.isbn, self.title, self.authors, self.pages, self.publ_year,
                self.publisher, self.location, self.description, self.call_num, self.tags]
    
    def create_from_list(self, myList):
        """
        Fill in details of this from a list.

        @param myList: list formatted just right
        """

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
            
    def remove_unicode(self):
        """
        Remove unicode in this book.

        Remove the unicode in this book by normalizing it to ASCII.  This eliminates the obnoxious u'
        """

        self.title = unicodedata.normalize('NFKD', unicode(self.title)).encode('ascii','ignore')
        self.authors = unicodedata.normalize('NFKD', unicode(self.authors)).encode('ascii','ignore')
        self.publisher = unicodedata.normalize('NFKD', unicode(self.publisher)).encode('ascii','ignore')
        self.location = unicodedata.normalize('NFKD', unicode(self.location)).encode('ascii','ignore')
        self.description = unicodedata.normalize('NFKD', unicode(self.description)).encode('ascii','ignore')
        self.call_num = unicodedata.normalize('NFKD', unicode(self.call_num)).encode('ascii','ignore')
        
    def __str__(self):
        return self.title + " by: " + self.authors