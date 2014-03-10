import ConfigParser
import os.path
import datetime
from lookup import Lookup
from book import Book
from bdb import Bdb
from person import Person
from loan import Loan
import appdirs
import sys


book_terms = ["title", "authors", "barcode", "isbn", "number of pages", "publication year",
              "publisher", "location", "description", "call number", "tags"]
book_substitutions = {"barcode": "bc", "number of pages": "pages", "publication year": "publ_year",
                      "call number": "call_num"}

person_terms = ["unique id", "first name", "last name", "email", "phone number", "address", "city", "state" "notes"]
person_substitutions = {"unique id": "id", "first name": "first_name", "last name": "last_name", "phone number": "phone_num"}


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


def search_book_helper():
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

    if search_field not in book_terms:
        print "Error, exiting."
        return
    elif search_term == "":
        print "Error, exiting."
        return
    else:
        if search_field in book_substitutions:
            search_field = book_substitutions[search_field]
        the_db = Bdb(dbLocation)
        return the_db.search_book(search_field, search_term)


def edit_book_helper(edit_bk):
    print ''''I'm going to show you each element of the book.  If you don't want
              to change it, just press enter.  Otherwise, enter a new value.
              For multiple authors and tags, separate them by a comma.
              e.g. author1,author2,author3'''
    new_book = {}
    new_book['barcode'] = raw_input("Barcode: " + str(edit_bk.bc))
    new_book['isbn'] = raw_input("ISBN: " + str(edit_bk.isbn))
    new_book['title'] = raw_input("Title: " + str(edit_bk.title))  # doesn't pull info for anything below.
    new_book['authors'] = raw_input("Authors: " + str(edit_bk.authors))
    new_book['pages'] = raw_input("Number of Pages: " + str(edit_bk.pages))
    new_book['publ_year'] = raw_input("Publication Year: " + str(edit_bk.publ_year))
    new_book['publisher'] = raw_input("Publisher: " + str(edit_bk.publisher))
    new_book['location'] = raw_input("Location: " + str(edit_bk.location))
    new_book['description'] = raw_input("Description: " + str(edit_bk.description))
    new_book['call_num'] = raw_input("Call number: " + str(edit_bk.call_num))
    new_book['tags'] = raw_input("Tags: " + str(edit_bk.tags))

    for key, value in new_book.iteritems():
        if value == '':
            new_book[key] = None

    old_bc = edit_bk.bc # we need this to ensure we don't create a duplicate db entry
    edit_bk.edit(new_book['barcode'], new_book['isbn'], new_book['title'], new_book['authors'],
                 new_book['pages'], new_book['publ_year'], new_book['publisher'],
                 new_book['location'], new_book['description'], new_book['call_num'],
                 new_book['tags'])
    edit_bk.remove_unicode()
    the_db = Bdb(dbLocation)
    if edit_bk.bc is None:
        the_db.store_book(edit_bk)
    else:
        the_db.delete_book(Book(old_bc))
        the_db.store_book(edit_bk)


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
        for item in book_terms:
            manual_add[item] = raw_input("Please enter the " + item + ": ")

        for item in manual_add:
            if item in book_substitutions:
                manual_add[book_substitutions[item]] = manual_add.pop(item)

        manual_book = create_book_from_dict(manual_add)
        manual_book.remove_unicode()
        book_db = Bdb(dbLocation)
        book_db.store_book(manual_book)

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
            book_db.store_book(book)

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
            book_db.store_book(book)


def delete_book():
    to_do = raw_input('''We're going to delete a book.  Do you have the barcode? [y/N]: ''')
    if to_do.strip() == "" or to_do.strip().lower() == "n":
        results = search_book_helper()
        i = 1
        for item in results:
            print(i + ") " + item)  # not sure how this will come out.
        del_me = raw_input("Which one is it? ")

        del_me = int(del_me)

        del_me = results[del_me - 1]
        del_me = del_me.split(",")
        del_me = Book(del_me[0])  # this is really fudged atm.  serious testing needed
        the_db = Bdb(dbLocation)
        the_db.delete_book(del_me)
        print "Deleted."

    elif to_do.strip().lower() == "y":
        del_me = raw_input("Ok, enter it now: ")
        if del_me.strip() == "":
            print "Invalid input."
        else:
            del_me = int(del_me)
            del_me = Book(del_me)
            the_db = Bdb(dbLocation)
            the_db.delete_book(del_me)
            print "Deleted."


def edit_book():
    to_do = raw_input("We're going to edit a book.  Do you have the barcode? [y/N]: ")
    if to_do.strip() == "" or to_do.strip().lower() == "n":
        results = search_book_helper()
        i = 1
        for item in results:
            print (str(i) + ") " + str(item))  # not sure how this will come out, same as above.
        edit_choice = raw_input("Which one is it? ")

        edit_choice = int(edit_choice)
        edit_choice = results[edit_choice - 1]
        edit_choice = list(edit_choice)
        edit_choice = create_book_from_list(edit_choice)
        edit_book_helper(edit_choice)

    elif to_do.strip().lower() == "y":
        edit_choice = raw_input("Ok, enter it now: ")
        if edit_choice.strip() == "":
            print "Invalid input."
        else:
            edit_choice = int(edit_choice)
            the_db = Bdb(dbLocation)
            edit_choice = the_db.retrieve_book(edit_choice)
            edit_choice = create_book_from_list(edit_choice)  # might not need this?
            edit_book_helper(edit_choice)


def search_book():
    results = search_book_helper()
    if 2 == results:
        print "Returning you to the beginning"
        return
    i = 1


def show_all_books():
    the_db = Bdb(dbLocation)
    for item in the_db.get_all_books():
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


def create_person_from_list(person_list):
    person = Person(person_list[0], person_list[1], person_list[2], person_list[3], person_list[4], person_list[5],
                    person_list[7], person_list[8])
    return person


def add_person():
    print "Let's add a new person!  Feel free to leave anything blank."
    print
    first_name = raw_input("What's the person's first name?")
    last_name = raw_input("\t\t...last name?")
    email = raw_input("\t\t...email?")
    phone_num = raw_input("\t\t...phone number?")
    address = raw_input("\t\t...address?")
    city = raw_input("\t\t...city?")
    state = raw_input("\t\t...state?")
    notes = raw_input("\t\t...any notes?")

    print "Do you have a unique ID you'd like to use for this person?"
    uid = raw_input("If yes, enter it, otherwise enter -1")
    new_person = Person(uid, first_name, last_name, email, phone_num, address, city, state, notes)

    people_db = Bdb(dbLocation)
    people_db.store_person(new_person)


def search_people():
    print "Welcome to searching!"
    print '''You can search by: unique id, first name, last name, email, phone number, address, city, state, or notes.'''
    search_field = raw_input("Which would you like to search by? ")
    search_field = search_field.lower()
    search_term = raw_input("OK, go ahead: ")

    if search_field not in person_terms:
        print "Error, exiting."
        return
    elif search_term == "":
        print "Error, exiting."
        return
    else:
        if search_field in person_substitutions:
            search_field = person_substitutions[search_field]
            theDB = Bdb(dbLocation)
            return theDB.search_person(search_field, search_term)


def lend_book():
    print "To whom would you like to lend a book?"
    todo = raw_input("Do you have their unique ID? [y/N]: ")
    if todo.strip() == "" or todo.strip().lower() == 'n':
        results = search_people()
        for i, item in enumerate(results):
            print (str(i) + ") " + str(item)) # not sure how this will come out, same as above.
        lend_person = raw_input("Who is it? ")

        lend_person = int(lend_person)
        lend_person = results[lend_person - 1]
        lend_person = list(lend_person)
        lend_person = create_person_from_list(lend_person)

        print "Which book would you like to lend?"
        to_do = raw_input("Do you have its barcode? [y/N]: ")
        if to_do.strip() == "" or to_do.strip().lower() == 'n':
            results = search_book_helper()
            for item in results:
                print str(i) + ") " + str(item)
            book_lend = raw_input("Which one is it? ")

            book_lend = int(book_lend)
            book_lend = results[book_lend - 1]
            book_lend = list(book_lend)
            book_lend = create_book_from_list(book_lend)

            the_db = Bdb(dbLocation)

            due_date = datetime.date.today() + datetime.timedelta(days=30)
            user_date = raw_input("When is it due? [" + str(due_date) + "]: ")
            if user_date.strip() == "":
                loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                the_db.store_loan(loan)
            else:
                user_date = user_date.strip()
                user_date = datetime.datetime.strptime(user_date, "%Y-%m-%d").date()
                loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                the_db.store_loan(loan)

        elif todo.strip().lower() == 'y':
            bc = raw_input("Ok, enter it now: ")
            if bc.strip() == '':
                print "Invalid input."
            else:
                the_db = Bdb(dbLocation)
                bc = int(bc)
                book_lend = the_db.retrieve_book(bc)
                book_lend = create_book_from_list(book_lend)

                due_date = datetime.date.today() + datetime.timedelta(days=30)
                user_date = raw_input("When is it due? [" + str(due_date) + "]: ") # assumptions
                if user_date.strip() == "":
                    loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                    the_db.store_loan(loan)
                else:
                    user_date = user_date.strip()
                    user_date = datetime.datetime.strptime(user_date, "%Y-%m-%d").date()
                    loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                    the_db.store_loan(loan)

    elif todo.strip().lower() == 'y':
        uid = raw_input("Ok, enter it now: ")
        if uid.strip() == '':
            print "Invalid input."
        else:
            uid = int(uid)
            the_db = Bdb(dbLocation)
            lend_person = the_db.retrieve_person(uid)
            lend_person = create_person_from_list(lend_person)
            print "Which book would you like to lend?"
            todo = raw_input("Do you have its barcode? [y/N]: ")
            if todo.strip() == "" or todo.strip().lower() == 'n':
                results = search_book_helper()
                for i, item in enumerate(results):
                    print str(i) + ") " + str(item)
                book_lend = raw_input("Which one is it? ")

                book_lend = int(book_lend)
                book_lend = results[book_lend - 1]
                book_lend = list(book_lend)
                book_lend = create_book_from_list(book_lend)

                the_db = Bdb(dbLocation)

                due_date = datetime.date.today() + datetime.timedelta(days=30)
                user_date = raw_input("When is it due? [" + str(due_date) + "]: ")
                if user_date.strip() == "":
                    loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                    the_db.store_loan(loan)
                else:
                    user_date = user_date.strip()
                    user_date = datetime.datetime.strptime(user_date, "%Y-%m-%d").date()
                    loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                    the_db.store_loan(loan)

            elif 'y' == todo.strip().lower():
                bc = raw_input("Ok, enter it now: ")
                if bc.strip() == '':
                    print "Invalid input."
                else:
                    bc = int(bc)
                    book_lend = the_db.retrieve_book(bc)
                    book_lend = create_book_from_list(book_lend)

                    due_date = datetime.date.today() + datetime.timedelta(days=30)
                    user_date = raw_input("When is it due? [" + str(due_date) + "]: ") # just going to assume it's in YYYY-MM-DD form for now.
                    if user_date.strip() == "":
                        loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)  # probably don't want user settable uid. remove from class?
                        the_db.store_loan(loan)
                    else:
                        user_date = user_date.strip()
                        user_date = datetime.datetime.strptime(user_date, "%Y-%m-%d").date()
                        loan = Loan(-1, book_lend, lend_person, datetime.date.today(), due_date, False)
                        the_db.store_loan(loan)


def show_all_loans():
    """
    Note that this only shows currently active loans, i.e. not historical ones
    """
    theDB = Bdb(dbLocation)
    for item in theDB.get_all_loans():
        print item
    raw_input("Press any key to continue.")


def edit_person():
    print "Who would you like to edit?"
    todo = raw_input("Do you have their unique ID? [y/N]: ")
    if todo.strip() == "" or todo.strip().lower() == 'n':
        results = search_people()
        i = 1
        for item in results:
            print (str(i) + ") " + str(item)) # not sure how this will come out, same as above.
        lend_person = raw_input("Who is it? ")

        lend_person = int(lend_person)
        lend_person = results[lend_person - 1]
        lend_person = list(lend_person)
        lend_person = create_person_from_list(lend_person)

    elif todo.strip().lower() == 'y':
        uid = raw_input("Ok, enter it now: ")
        if uid.strip() == '':
            print "Invalid input."
        else:
            uid = int(uid)
            the_db = Bdb(dbLocation)
            lend_person = the_db.retrieve_person(uid)
            lend_person = create_person_from_list(lend_person)


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
        6) Lending\n
        7) Change database location\n
        8) Exit: ''')

        try:
            todo = int(todo)
        except ValueError:  # I think int() throws that.
            print "Invalid input."
            continue

        if todo < 1 or (todo > 8 and todo != 42):
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
            todo = raw_input('''Here's what you can do: \n
            1) Lend a book (checkout)\n
            2) Return a lent book (checkin)\n
            3) Show currently lent books\n
            4) Add a person (new patron/lendee)\n
            5) Search for a person\n
            6) Edit a person\n
            7) Delete a person\n
            8) Search historical transactions\n
            9) Go back: ''')

            try:
                todo = int(todo)
            except ValueError:
                print "Invalid input."
                continue

            if todo == 1:
                lend_book()
            elif todo == 2:
                pass
            elif todo == 3:
                show_all_loans()  # @TODO: This needs a nicer printout.
            elif todo == 4:
                add_person()
            elif todo == 5:
                search_people()
            elif todo == 6:
                pass
            elif todo == 7:
                pass
            elif todo == 8:
                pass
            elif todo == 9:
                pass
            else:
                print "Invalid choice."
                continue

        elif todo == 7:
            if 0 == change_db_location(dbLocation):
                print "Changed successfully."

        elif todo == 8:
            print "So long, and thanks for all the fish!"
            run = False

        elif todo == 42:
            debug_menu()

        else:
            print "Invalid choice"
            continue
