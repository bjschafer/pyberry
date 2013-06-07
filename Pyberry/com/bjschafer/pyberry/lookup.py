from apiclient.discovery import build

class Lookup(object):
    '''
    Looks up book information online.  Currently only uses Google Books API.
    Also, currently only allows searching by ISBN.
    
    Searching is accomplished using the RESTful API from Google Books.  This
    is relatively simple for sending the search request but rather more troublesome
    for processing the received data.  
    
    @TODO: add other search resources (2.0)
    @TODO: allow search by any attribute (1.0)
    @TODO: better error handling. (1.0)
    '''
    
    def __init__(self, akey = None):
        '''
        constructor
        '''
        self.apiKey = akey
        
    def _createDict(self, response):
        bookDict = {}
        bookDict['title'] = response['volumeInfo']['title']
        authors = response['volumeInfo']['authors']
        authors = authors.strip()
        authors = authors.split(',')
        # verify we don't get square brackets
        bookDict['authors'] = authors
        bookDict['pages'] = response['pageCount']
        bookDict['publ_year'] = response['publishedDate'][0:4] # not quite sure if this will just get us the year
        bookDict['publisher'] = response['publisher']
        bookDict['description'] = response['description']
        
        return bookDict
    
    def chooseResponse(self, bookID):
        '''
        @param bookID: the ID of the book as selected by user from previous data.
        @return: Returns the created dict of the selected book.
        
        This is a bit screwed up but at least it's done in an OO way.
        The byTitle method returns the list of book information.  The user then
        chooses which one they want, and the program finds the unique ID of that
        option.  It's then passed into this method, which picks the right book
        and creates the dict of it.
        
        It's bad because it's inconsistent with the searching by ISBN behavior.
        But it doesn't do awful things, so it'll do for now. 
        '''
        for book in self.response.get('items', []):
            if book['id'] == bookID:
                return self._createDict(book)
            else:
                pass
                
        
    def byISBN(self, isbn):
        '''
        searches Google Books using the book's isbn.  Pretty foolproof.
        '''
        if len(isbn) != 10 and len(isbn) != 13:
            raise ValueError("Invalid ISBN length.")
        else:
            service = build('books', 'v1', developerKey=self.apiKey)
            request = service.volumes().list(source='public', q='isbn:'+str(isbn))
            response = request.execute()
            
            bookDict = self._createDict(response)
            bookDict['isbn'] = isbn
            return bookDict
        
    def byTitle(self, title):
        '''
        searches Google Books via title.  Potentially lots of info here.
        '''
        service = build('books', 'v1', developerKey = self.apiKey)
        request = service.volumes().list(source='public', q='title:'+title)
        self.response = request.execute()
        
        return self.response['items']
