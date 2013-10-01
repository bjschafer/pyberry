import ConfigParser
import os.path
import random
from com.bjschafer.pyberry.lookup import Lookup
from com.bjschafer.pyberry.book import Book
from com.bjschafer.pyberry.bdb import Bdb

#TODO: change settings in program.

terms = ["title", "authors", "barcode", "isbn", "number of pages", "publication year",
         "publisher", "location", "description", "call number", "tags"]
substitutions = {"barcode": "bc", "number of pages": "pages", "publication year": "publ_year",
                 "call number": "call_num"}

def readWriteConfig():
    if not os.path.isfile('.pyberry'): # check if the file exists, if not we're creating it.
        config = ConfigParser.RawConfigParser()
        config.add_section("local")
        config.add_section("api")
        
        config.set('local', 'dbPath', '.pyberry.sqlite')
        config.set('api', 'apiKey', '')
        
        with open('.pyberry', 'wb') as configFile:
            config.write(configFile)
        readWriteConfig() # this should now go and fill in default values, but needs testing
    else:
        config = ConfigParser.RawConfigParser()
        config.read('.pyberry')
        loc = config.get('local', 'dbPath')
        key = config.get('api', 'apiKey')
        return (loc, key)
    
def randomBC():
    '''
    This probably isn't elegant, but it should give random numbers
    that are rather not likely to collide.
    '''
    gen = random.Random()
    temp = gen.randrange(100000,999999)
    return abs(temp+gen.randrange(100000,999999))

def search():
    '''
    This does the searching and user-interaction for it.
    It returns a list of search results.
    '''
    print "Welcome to searching!"
    print '''You can search by: title, author, barcode, isbn, number of pages, publication year,
    location, description, call number, or tags.'''
    search_field = raw_input("Which would you like to search by? ")
    search_term = raw_input("OK, go ahead: ")
    
    if search_field not in terms:
        print "Error, exiting."
        return
    elif search_term == "":
        print "Error, exiting."
        return
    else:
        if search_field in substitutions:
            search_field = substitutions[search_field]
        theDB = Bdb(dbLocation)
        return theDB.search(search_field, search_term)
  
def edit(editBook):
    print ''''I'm going to show you each element of the book.  If you don't want
              to change it, just press enter.  Otherwise, enter a new value.'''
    newBook = {}
    newBook['barcode'] = raw_input("Barcode: " + str(editBook.bc))
    newBook['isbn'] = raw_input("ISBN: " + str(editBook.isbn))
    newBook['title'] = raw_input("Title: " + str(editBook.title)) # doesn't pull info for anything below.
    newBook['authors'] = raw_input("Authors: " + str(editBook.authors)) # list...
    newBook['pages'] = raw_input("Number of Pages: " + str(editBook.pages))
    newBook['publ_year'] = raw_input("Publication Year: " + str(editBook.publ_year))
    newBook['publisher'] = raw_input("Publisher: " + str(editBook.publisher))
    newBook['location'] = raw_input("Location: " + str(editBook.location))
    newBook['description'] = raw_input("Description: " + str(editBook.description))
    newBook['call_num'] = raw_input("Call number: " + str(editBook.call_num))
    newBook['tags'] = raw_input("Tags: " + str(editBook.tags)) # list...
    
    for key,value in newBook.iteritems():
        if value == '':
            newBook[key] = None
    
    oldBC = editBook.bc
    editBook.edit(newBook['barcode'], newBook['isbn'], newBook['title'], newBook['authors'], 
                  newBook['pages'], newBook['publ_year'], newBook['publisher'], 
                  newBook['location'], newBook['description'], newBook['call_num'],
                  newBook['tags'])
    
    theDB = Bdb(dbLocation)
    if editBook.bc == None:
        theDB.store(editBook)
    else:
        theDB.delete(Book(oldBC))
        theDB.store(editBook)
        
def printLogo():
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

def createBookFromDict(book_dict):
    book = Book(book_dict["bc"], book_dict["isbn"], book_dict["title"], book_dict["authors"],
                book_dict["pages"], book_dict["publ_year"], book_dict["publisher"], book_dict["location"], 
                book_dict["description"], book_dict["call_num"], book_dict["tags"])
    return book

def createBookFromList(book_list):
    book = Book(book_list[0], book_list[1], book_list[2], book_list[3], book_list[4], book_list[5], book_list[6], 
                book_list[7], book_list[8], book_list[9], book_list[10])
    return book

def addBook():
    addOption = raw_input('''Let's add a book.  How would you like to add it?\n
    1) Manually\n
    2) Search by ISBN\n
    3) Search by Title: ''')
    
    addOption = int(addOption)
    
    if addOption == 1:
        manualAdd = {}
        for item in terms:
            manualAdd[item] = raw_input("Please enter the " + item)
            
        for item in manualAdd:
            if item in substitutions:
                manualAdd[substitutions[item]] = manualAdd.pop(item)
        
        manualBook = createBookFromDict(manualAdd)
        bookDB = Bdb(dbLocation)
        bookDB.store(manualBook)
        
    elif addOption == 2:
        isbn = raw_input("Please enter the 10 or 13 digit ISBN: ")
        lookup = Lookup()
        bookInfo = lookup.byISBN(isbn)
        bc = ('''Please enter a unique barcode, or -1 to autogenerate: ''')
        
        bc = int(bc)
        
        if bc == -1:
            bookInfo["bc"] = randomBC()
        else:
            bookInfo["bc"] = bc
        
        location = raw_input('''Please enter the location of the book, default blank: ''')
        bookInfo["location"] = location
        
        call_num = raw_input('''Please enter the call number of the book: ''')
        bookInfo["call_num"] = call_num
        
        tags = raw_input('''Please enter any tags, separated by a comma: ''')
        tags = tags.strip()
        tags = tags.split(',')
        bookInfo["tags"] = tags
    
        print '''Ok, everything should be set.  I'll show you what I've got,
        and if it looks good, just press enter, otherwise type something in
        and I'll return you to the beginning.'''
        
        for item in bookInfo:
            print str(item) + ": " + str(bookInfo[item])
            
        isOk = raw_input("")
        
        if isOk != "": # not 100% sure this will work
            raise ValueError
        else:
            addBook = createBookFromDict(bookInfo)
            bookDB = Bdb(dbLocation)
            bookDB.store(addBook)
            
    elif addOption == 3:
        title = raw_input("Please enter the title you'd like to search for:")
        lookup = Lookup()
        books = lookup.byTitle(title)
        count = 1
        raw_input('''The following are the results.  Please enter the number of the\n
        result you'd like.  Press any key to display them.''')
        for book in books:
            print '%i) Title: %s, Authors: %s' % (
                                                  count,
                                                  book['volumeInfo']['title'],
                                                  str(book['volumeInfo']['authors']).strip('[]'))
            count += 1
        userChoice = raw_input("Which result would you like? ")
        
        userChoice = int(userChoice)

        userChoice = userChoice - 1 # need to compensate for off-by-one.
        
        bookInfo = lookup.chooseResponse(books[userChoice]['id'])
        
        bc = raw_input('''Please enter a unique barcode, or -1 to autogenerate: ''')
        
        bc = int(bc)
        
        if bc == -1:
            bookInfo["bc"] = randomBC()
        else:
            bookInfo["bc"] = bc
        
        location = raw_input('''Please enter the location of the book, default blank: ''')
        bookInfo["location"] = location
        
        call_num = raw_input('''Please enter the call number of the book: ''')
        bookInfo["call_num"] = call_num
        
        tags = raw_input('''Please enter any tags, separated by a comma: ''')
        tags = tags.strip()
        tags = tags.split(',')
        bookInfo["tags"] = tags
        
        for key, value in bookInfo.iteritems():
            try:
                value = value.encode('ascii','ignore')
            except AttributeError:
                pass
            bookInfo[key] = value
    
        if not 'isbn' in bookInfo:
            bookInfo['isbn'] = 0
        print '''Ok, everything should be set.  I'll show you what I've got,
        and if it looks good, just press enter, otherwise type something in
        and I'll return you to the beginning.'''
        
        for item in bookInfo:
            print str(item) + ": " + str(bookInfo[item])
            
        isOk = raw_input("")
        
        if isOk != "": # not 100% sure this will work
            raise ValueError
        else:
            addBook = createBookFromDict(bookInfo)
            bookDB = Bdb(dbLocation)
            bookDB.store(addBook)

def deleteBook():
    todo = raw_input('''We're going to delete a book.  Do you have the barcode? [y/N]: ''')
    if todo.strip() == "" or todo.strip().lower() == "n":
        results = search()
        i = 1
        for item in results:
            print(i + ") " + item) # not sure how this will come out.
        delMe = raw_input("Which one is it? ")
        
        delMe = int(delMe)
        
        delMe = results[delMe - 1]
        delMe = delMe.split(",")
        delMe = Book(delMe[0]) # this is really fudged atm.  serious testing needed
        theDB = Bdb(dbLocation)
        theDB.delete(delMe)
        print "Deleted."
        
    elif todo.strip().lower() == "y":
        delMe = raw_input("Ok, enter it now: ")
        if delMe.strip() == "":
            print "Invalid input."
        else:
            delMe = int(delMe)
            delMe = Book(delMe)
            theDB = Bdb(dbLocation)
            theDB.delete(delMe)
            print "Deleted."
    
def editBook():
    todo = raw_input("We're going to edit a book.  Do you have the barcode? [y/N]: ")
    if todo.strip() == "" or todo.strip().lower() == "n":
        results = search()
        i = 1
        for item in results:
            print (str(i) + ") " + str(item)) # not sure how this will come out, same as above.
        editChoice = raw_input("Which one is it? ")
        
        editChoice = int(editChoice)
        editChoice = results[editChoice - 1]
        editChoice = list(editChoice)
        editChoice = createBookFromList(editChoice)
        edit(editChoice)
        
    elif todo.strip().lower() == "y":
        editChoice = raw_input("Ok, enter it now: ")
        if editChoice.strip() == "":
            print "Invalid input."
        else:
            editChoice = int(editChoice)
            theDb = Bdb(dbLocation)
            editChoice = theDb.retrieve(editChoice)
            editChoice = createBookFromList(editChoice) # might not need this?
            edit(editChoice)      
                          
def searchBook():
    results = search()
    i = 1
    for item in results:
        print str(i) + ") " + str(item)
                  
def showAllBooks():
    theDB = Bdb(dbLocation)
    for item in theDB.getAll():
        print item
        
def changeDBLocation():
    config = ConfigParser.RawConfigParser()
    config.read('.pyberry')
    loc = config.get('local', 'dbPath')
    print "Current location is %s" % loc
    changeIt = raw_input("Would you like to change it? [y/N]: ")
    
    if changeIt.strip().lower() != 'y':
        return 1
    else:
        newLoc = raw_input(''''Please enter a new path, either relative to current directory\n
        or an absolute path.  I'll fail if there's a permissions issue, though.\n
        Current path %s''' % loc)
        
        try:
            f = open(newLoc, 'r')
        except IOError:
            print "Sorry, %s won't work.\nI'll return you to the menu." % newLoc
            return 1
        finally:
            f.close()
            
        config.set('local', 'dbPath', newLoc)
        with open('.pyberry','wb') as configFile:
            config.write(configFile)
        return 0


if __name__ == '__main__':
    dbLocation, apiKey = readWriteConfig() #verify syntax of this
    
    run = True
    
    printLogo()
    
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
        except:
            print "Invalid input."
            continue
        
        if todo < 1 or todo > 7:
            print "Invalid input."
            continue
        
        if todo == 1:
            try:
                addBook()
            except TypeError:
                print "Invalid input."
                continue
            except ValueError: # They do the same thing, but for future's sake...
                print "Invalid input."
                continue
                
        elif todo == 2:
            deleteBook()
                    
        elif todo == 3:
            editBook()
            
        elif todo == 4:
            searchBook()
                
        elif todo == 5:
            showAllBooks()
                
        elif todo == 6:
            exitStatus = changeDBLocation()
            if exitStatus == 0:
                print "Changed successfully."
                    
        elif todo == 7:
            run = False
        
        else:
            print "Invalid choice"
            continue
            
