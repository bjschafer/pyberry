import urllib2
import simplejson
from book import Book  # right?  it's in this package

__author__ = 'braxton'


class Lookup(object):

    def __init__(self):
        self.lookup_url = "http://openlibrary.org/api/books?bibkeys="
        self.search_url = "http://openlibrary.org/search.json?"

    def _get_publisher_from_json_dict(self, data):
        """
        Get the publisher data from a JSON dict.

        @param data: a JSON dictionary
        @return: the author
        """

        return data.get('name')

    def _get_author_from_json_dict(self, data):
        """
        Get the author data from a JSON dict.

        @param data: a JSON dictionary
        @return: the author
        """

        return data.get('name', None)

    def _get_book_from_json_dict(self, data):
        """
        Create a new Book instance based on a JSON dict.

        @param data: a JSON dictionary
        @return: a new Book instance (sans ISBN)
        """
        publishers = ', '.join([self._get_publisher_from_json_dict(p) for p in data['publishers']])
        authors = ', '.join([self._get_author_from_json_dict(a) for a in data['authors']])
        book = Book(0)  # better to create an object, even if there's no valid barcode yet
        book.title = data.get('title', None)
        book.publisher = publishers
        book.authors = authors
        book.pages = data.get('number_of_pages', None)  # might cause issue, be careful.
        book.publ_year = data.get('publish_date', None)
        book.description = data.get('excerpts', None)
        return book

    @classmethod
    def choose_item(cls, items, choice):
        """
        Choose a book from the list returned from searching.

        @param items: the list of items to choose from
        @param choice: the choice to pull and format
        @return: the selected item formatted from the list
        """

        for book in items.get('items', []):
            if book['id'] == choice:
                return cls._get_book_from_json_dict(book)
            else:
                pass

    def by_isbn(self, isbn):
        """
        Search for one book on OpenLibrary by ISBN

        @param isbn: the book's ISBN to retrieve
        @return: a dict containing data from that book.
        """

        if len(isbn) != 10 and len(isbn) != 13:
            raise ValueError
        url = urllib2.urlopen(self.lookup_url+"ISBN"+":%s&jscmd=data&format=json" % isbn)
        data = simplejson.load(url)['%s:%s' % ("ISBN", isbn)]
        book = self._get_book_from_json_dict(data)
        book.isbn = isbn
        return book

    def by_title(self, title):
        """
        Search for a book on OpenLibrary by title

        @param title: the title to search for
        @return: the raw data of all results
        """
        title = title.replace(' ', '+').lower()
        url = urllib2.urlopen(self.search_url+'title='+title)
        data = simplejson.load(url)['docs']

        for result in data:
            book = Book(0)
            book.title = result['title']
            try:
                book.authors = ', '.join(result['author_name']) if isinstance(result['publisher'], list) else result['author_name']
            except KeyError:
                book.authors = "None"
            try:
                book.publisher = ', '.join(result['publisher']) if isinstance(result['publisher'], list) else result['publisher']
            except KeyError:
                book.publisher = "No publisher found."
            try:
                book.publ_year = result['first_publish_year']
            except KeyError:
                book.publ_year = 0
            try:
                book.description = ''.join(result['first_sentence'])
            except KeyError:
                book.description = "No description found."

            yield book