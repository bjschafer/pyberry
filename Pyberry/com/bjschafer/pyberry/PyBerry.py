import ConfigParser
import os.path
from lookup import Lookup
from book import Book
from bdb import Bdb
import appdirs
import sys


terms = ["title", "authors", "barcode", "isbn", "number of pages", "publication year",
         "publisher", "location", "description", "call number", "tags"]
substitutions = {"barcode": "bc", "number of pages": "pages", "publication year": "publ_year",
                 "call number": "call_num"}


def write_config():
    config_path = appdirs.user_data_dir("Pyberry", "Braxton Schafer")
    if sys.platform == 'win32' or sys.platform == 'win64':
        config_path += '''\\'''
    else:
        config_path += '/'
    config = ConfigParser.RawConfigParser()
    config.add_section("local")

    config.set('local', 'dbPath', config_path + '.pyberry.sqlite')

    with open(config_path + '.pyberry', 'wb') as configFile:
        config.write(configFile)


def read_config():
    config_path = appdirs.user_data_dir("Pyberry", "Braxton Schafer")
    if sys.platform == 'win32' or sys.platform == 'win64':
        config_path += '''\\'''
    else:
        config_path += '/'
    print config_path
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.isfile(config_path + '.pyberry'):
        write_config()
    config = ConfigParser.RawConfigParser()
    config.read(config_path + '.pyberry')
    return config.get('local', 'dbPath')


def search():
    """
    Do searching and user-interaction for it.

    @return: a list of search results
    """

    print "Welcome to searching!"
    print '''You can search by: title, authors, barcode, isbn, number of pages, publication year,
    location, description, call number, or tags.'''
    search_field = raw_input("Which would you like to search by? ")
    search_term = raw_input("OK, go ahead: ")

    if '' == search_field or '' == search_term:
        return 2

    if search_field not in terms:
        print "Error, exiting."
        return
    elif search_term == "":
        print "Error, exiting."
        return
    else:
        if search_field in substitutions:
            search_field = substitutions[search_field]
        the_db = Bdb(dbLocation)
        return the_db.search(search_field, search_term)


def edit(edit_book):
    print ''''I'm going to show you each element of the book.  If you don't want
              to change it, just press enter.  Otherwise, enter a new value.
              For multiple authors and tags, separate them by a comma.
              e.g. author1,author2,author3'''
    new_book = {}
    new_book['barcode'] = raw_input("Barcode: " + str(edit_book.bc))
    new_book['isbn'] = raw_input("ISBN: " + str(edit_book.isbn))
    new_book['title'] = raw_input("Title: " + str(edit_book.title))  # doesn't pull info for anything below.
    new_book['authors'] = raw_input("Authors: " + str(edit_book.authors))
    new_book['pages'] = raw_input("Number of Pages: " + str(edit_book.pages))
    new_book['publ_year'] = raw_input("Publication Year: " + str(edit_book.publ_year))
    new_book['publisher'] = raw_input("Publisher: " + str(edit_book.publisher))
    new_book['location'] = raw_input("Location: " + str(edit_book.location))
    new_book['description'] = raw_input("Description: " + str(edit_book.description))
    new_book['call_num'] = raw_input("Call number: " + str(edit_book.call_num))
    new_book['tags'] = raw_input("Tags: " + str(edit_book.tags))

    for key, value in new_book.iteritems():
        if value == '':
            new_book[key] = None

    old_bc = edit_book.bc # we need this to ensure we don't create a duplicate db entry
    edit_book.edit(new_book['barcode'], new_book['isbn'], new_book['title'], new_book['authors'],
                   new_book['pages'], new_book['publ_year'], new_book['publisher'],
                   new_book['location'], new_book['description'], new_book['call_num'],
                   new_book['tags'])
    edit_book.remove_unicode()
    the_db = Bdb(dbLocation)
    if edit_book.bc is None:
        the_db.store(edit_book)
    else:
        the_db.delete(Book(old_bc))
        the_db.store(edit_book)


def print_logo():
    print '''
                                   ,...... 77                                   
                              7,..............7                                 
                            7...................                                
                           +.....................                               
                           .......................                              
                          .........=,......~......                              
                          ...:= 7I?.........,.....                              
                          ...+77 7 7=.....~7 ~....                              
                          .:I7==?+???...:?7I?~....                              
                          .~=?    77 I.~7  7 7~..7                              
                          :.~:~+I7  7=,:II=:::..I                               
                           .II+=~~~~~~,===+7+,.                                 
                            .:?777 7 7I777I+..                                  
                            ,.:+II777I7I=+=..                                   
                             ..:::~~~~~:~+..7                                   
                              ,,???II???+..7                                    
                               7.::~~:~:..                                      
                                 .:~+~~,.                                       
                                  .~?I?.+                                       
                                  7.~??.=                                       
                                 7=.:??,.                                       
                           7.....:..+II7=.                                      
                           .........~+I=::7    ....7                            
                   7....,:~........~+7~.~=...........                           
                   ............,++I7  7+?=...........I                          
                  .....................................                         
                7 ......................................                        
                ........................................                        
               .........................................                        
               :.......................................,,7                      
               :......................................:+=,.                     
              .:=~.................................:=III?=...=77                
             ..II777++,......................,::+III?+?+++++,...7               
           =.~?III?7I+?+~,.,=:,:~::==~~?+?7II7?+~~~:::::,,........7             
         7..==~.,..:~+++++=:,~=~?I7777I777I?=:~++II+=,:.,:,,........77          
       7.....:++??++I?I+=?I??I+=~::?II7II=~,=???,~~~~+=++~~....,~:.....         
      ...~+=?,,......,::~:,::,,:+?+:,+++~=??:....,::.,..........:~:::~... 7     
     ...~......,.,,...,::,:~~.....~:,.:.~=:..,+~:.......... 7       77.,,..7    
   ?.,~   77   77 7........:~::~=::,,,..~,=,~~,........7               7 ....+  
  ..:7                   ,.....,,~+=,:::::........ 7                        7   
  77                           ...............                                  
                                  ..........I                                   
                                 77777777I??7     '''


def create_book_from_dict(book_dict):
    book = Book(book_dict["bc"], book_dict["isbn"], book_dict["title"], book_dict["authors"],
                book_dict["pages"], book_dict["publ_year"], book_dict["publisher"], book_dict["location"],
                book_dict["description"], book_dict["call_num"], book_dict["tags"])
    return book


def create_book_from_list(book_list):  # PROTIP:  also works for tuples
    book = Book(book_list[0], book_list[1], book_list[2], book_list[3], book_list[4], book_list[5], book_list[6],
                book_list[7], book_list[8], book_list[9], book_list[10])
    return book


def add_book():
    add_option = raw_input('''Let's add a book.  How would you like to add it?\n
                              1) Manually\n
                              2) Search by ISBN\n
                              3) Search by Title: ''')

    add_option = int(add_option)

    if add_option == 1:
        manual_add = {}
        print "If you have multiple authors or tags, please separate them with a comma."
        print "e.g. author1,author2,author3"
        print "To autogenerate a barcode, enter -1 for it."
        print
        for item in terms:
            manual_add[item] = raw_input("Please enter the " + item + ": ")

        for item in manual_add:
            if item in substitutions:
                manual_add[substitutions[item]] = manual_add.pop(item)

        manual_book = create_book_from_dict(manual_add)
        manual_book.remove_unicode()
        book_db = Bdb(dbLocation)
        book_db.store(manual_book)

    elif add_option == 2:
        isbn = raw_input("Please enter the 10 or 13 digit ISBN: ")
        lookup = Lookup()
        book = lookup.by_isbn(isbn)
        bc = raw_input('''Please enter a unique barcode, or -1 to autogenerate: ''')

        bc = int(bc)

        book.bc = bc

        location = raw_input('''Please enter the location of the book, default blank: ''')
        book.location = location

        call_num = raw_input('''Please enter the call number of the book: ''')
        book.call_num = call_num

        tags = raw_input('''Please enter any tags, separated by a comma: ''')
        tags = tags.strip()
        book.tags = tags

        print '''Ok, everything should be set.  I'll show you what I've got,
        and if it looks good, just press enter, otherwise type something in
        and I'll return you to the beginning.'''

        book.print_check()

        is_ok = raw_input("")

        if is_ok != "":  # not 100% sure this will work
            raise ValueError
        else:
            book.remove_unicode()
            book_db = Bdb(dbLocation)
            book_db.store(book)

    elif add_option == 3:
        title = raw_input("Please enter the title you'd like to search for:")
        lookup = Lookup()
        raw_input("The following are the results.  Please enter the number of the " +
                  "result you'd like.  Press any key to display them.")
        books = []
        for index, book in enumerate(lookup.by_title(title), start=1):
            if index == 11:
                break  # only print first 10 results?? Not very elegant.
            print '%i) Title: %s, Author(s): %s' % (
                index,
                book.title,
                str(book.authors).strip('[]')
            )
            books.append(book)
        user_choice = raw_input("Which result would you like? Or hit enter for none.")

        if user_choice == '':
            return 2

        user_choice = int(user_choice)

        user_choice -= 1  # need to compensate for off-by-one.

        book = books[user_choice]

        bc = raw_input('''Please enter a unique barcode, or -1 to autogenerate: ''')
        bc = int(bc)
        book.bc = bc

        location = raw_input('''Please enter the location of the book, default blank: ''')
        book.location = location

        call_num = raw_input('''Please enter the call number of the book: ''')
        book.call_num = call_num

        tags = raw_input('''Please enter any tags, separated by a comma: ''')
        tags = tags.strip()
        book.tags = tags

        assert isinstance(book, Book)
        print '''Ok, everything should be set.  I'll show you what I've got,
        and if it looks good, just press enter, otherwise type something in
        and I'll return you to the beginning.'''

        book.print_check()

        is_ok = raw_input("")

        if is_ok != "":
            raise ValueError  # should consider changing to a UserQuit exception.
        else:
            book.remove_unicode()
            book_db = Bdb(dbLocation)
            book_db.store(book)


def delete_book():
    to_do = raw_input('''We're going to delete a book.  Do you have the barcode? [y/N]: ''')
    if to_do.strip() == "" or to_do.strip().lower() == "n":
        results = search()
        i = 1
        for item in results:
            print(i + ") " + item)  # not sure how this will come out.
        del_me = raw_input("Which one is it? ")

        del_me = int(del_me)

        del_me = results[del_me - 1]
        del_me = del_me.split(",")
        del_me = Book(del_me[0])  # this is really fudged atm.  serious testing needed
        the_db = Bdb(dbLocation)
        the_db.delete(del_me)
        print "Deleted."

    elif to_do.strip().lower() == "y":
        del_me = raw_input("Ok, enter it now: ")
        if del_me.strip() == "":
            print "Invalid input."
        else:
            del_me = int(del_me)
            del_me = Book(del_me)
            the_db = Bdb(dbLocation)
            the_db.delete(del_me)
            print "Deleted."


def edit_book():
    to_do = raw_input("We're going to edit a book.  Do you have the barcode? [y/N]: ")
    if to_do.strip() == "" or to_do.strip().lower() == "n":
        results = search()
        i = 1
        for item in results:
            print (str(i) + ") " + str(item))  # not sure how this will come out, same as above.
        edit_choice = raw_input("Which one is it? ")

        edit_choice = int(edit_choice)
        edit_choice = results[edit_choice - 1]
        edit_choice = list(edit_choice)
        edit_choice = create_book_from_list(edit_choice)
        edit(edit_choice)

    elif to_do.strip().lower() == "y":
        edit_choice = raw_input("Ok, enter it now: ")
        if edit_choice.strip() == "":
            print "Invalid input."
        else:
            edit_choice = int(edit_choice)
            the_db = Bdb(dbLocation)
            edit_choice = the_db.retrieve(edit_choice)
            edit_choice = create_book_from_list(edit_choice)  # might not need this?
            edit(edit_choice)


def search_book():
    results = search()
    if 2 == results:
        print "Returning you to the beginning"
        return
    i = 1
    for item in results:
        print str(i) + ") " + str(item)


def show_all_books():
    the_db = Bdb(dbLocation)
    for item in the_db.get_all():
        print item
    raw_input("Press any key to continue.")


def change_db_location(loc):
    config = ConfigParser.RawConfigParser()
    config.read('.pyberry')
    print "Current location is %s" % loc
    change_it = raw_input("Would you like to change it? [y/N]: ")

    if change_it.strip().lower() != 'y':
        return
    else:
        new_loc = raw_input(''''Please enter a new path, either relative to current directory\n
        or an absolute path.  I'll fail if there's a permissions issue, though.\n
        Current path %s''' % loc)

        try:
            f = open(new_loc, 'w+')
        except IOError:
            print "Sorry, %s won't work.\nI'll return you to the menu." % new_loc
            return 1
        finally:
            f.close()

        config.set('local', 'dbPath', new_loc)
        with open('.pyberry', 'wb') as configFile:
            config.write(configFile)
        return 0


def debug_menu():
    print "Hi, this is a secret.  What can I let you in on? "
    dbg = raw_input('''1) Config file location''')
    try:
        dbg = int(dbg)
    except ValueError:
        return

    if dbg == 1:
        print appdirs.user_data_dir("Pyberry", "Braxton Schafer")


if __name__ == '__main__':
    dbLocation = read_config()

    run = True

    print_logo()

    print "Welcome to PyBerry!"

    while run:
        todo = raw_input('''What would you like to do?  Your choices are:\n
        1) Add a book\n
        2) Delete a book\n
        3) Edit a book\n
        4) Search for a book\n
        5) Show all books\n
        6) Change database location\n
        7) Exit: ''')

        try:
            todo = int(todo)
        except ValueError:  # I think int() throws that.
            print "Invalid input."
            continue

        if todo < 1 or (todo > 7 and todo != 42):
            print "Invalid input."
            continue

        if todo == 1:
            try:
                if 2 == add_book():
                    print "Returning you to the beginning."
                    continue
            except TypeError:
                print "Invalid input."
                continue
            except ValueError:  # They do the same thing, but for future's sake...
                print "Invalid input."
                continue

        elif todo == 2:
            delete_book()

        elif todo == 3:
            edit_book()

        elif todo == 4:
            search_book()

        elif todo == 5:
            show_all_books()

        elif todo == 6:
            if 0 == change_db_location(dbLocation):
                print "Changed successfully."

        elif todo == 7:
            print "So long, and thanks for all the fish!"
            run = False

        elif todo == 42:
            debug_menu()

        else:
            print "Invalid choice"
            continue
