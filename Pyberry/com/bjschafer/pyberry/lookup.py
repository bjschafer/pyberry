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
        Creates a new Publisher instance based on a JSON dict.

        Args:
            data: a Json dictionary
        Returns:
            The data
        """
        return data.get('name')

    def _get_author_from_json_dict(self, data):
        """
        Creates a new Author instance based on a JSON dict.

        Args:
            data: a Json dictionary
        Returns:
            The data
        """
        return data.get('name', None), data.get('url', None)

    def _get_book_from_json_dict(self, data):
        """
        Create a new Book instance based on a JSON dict.

        @param data: a JSON dictionary
        @return: a new Book instance (sans ISBN)
        """
        publishers = [self._get_publisher_from_json_dict(p) for p in data['publishers']]
        authors = [self._get_author_from_json_dict(a) for a in data['authors']]
        book = Book(-1)  # better to create an object, even if there's no valid barcode yet
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
        title = title.replace(' ', '+').lower()
        url = urllib2.urlopen(self.search_url+'title='+title)
        return simplejson.load(url)
