import ConfigParser
import os.path.isfile
import random
from com.bjschafer.pyberry.lookup import Lookup
from com.bjschafer.pyberry.book import Book
from com.bjschafer.pyberry.bdb import Bdb

#TODO: change settings in program.

terms = ["title", "author", "barcode", "isbn", "number of pages", "publication year",
         "location", "description", "call number", "tags"]
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
        config.read('.pyberry')
        loc = config.get('local', 'dbPath')
        key = config.get('api', 'apiKey')
        return (loc, key)
    
def randomBC():
    '''
    This probably isn't elegant, but it should give random numbers
    that are rather not likely to collide.
    '''
    gen = random()
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
    search_field = input("Which would you like to search by? ")
    search_term = input("OK, go ahead: ")
    
    if search_field not in terms:
        print "Error, exiting."
        continue
    elif search_term == "":
        print "Error, exiting."
        continue
    else:
        if search_field in substitutions:
            search_field = substitutions[search_field]
        theDB = Bdb(dbLocation)
        return theDB.search(search_field, search_term)
    
if __name__ == '__main__':
    dbLocation, apiKey = readWriteConfig() #verify syntax of this
    
    run = True
    # logo
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
    
    print "Welcome to PyBerry!"
    
    while run:
        todo = input('''What would you like to do?  Your choices are:\n
        1) Add a book\n
        2) Delete a book\n
        3) Search for a book\n
        4) Show all books\n
        5) Change database location\n
        6) Exit: ''')
        
        try:
            todo = int(todo)
        except:
            print "Invalid input."
            continue
        
        if todo < 1 or todo > 6:
            print "Invalid input."
            continue
        
        if todo == 1:
            addOption = input('''Let's add a book.  How would you like to add it?\n
            1) Manually\n
            2) Search by ISBN\n
            3) Search by Title: ''')
            
            try:
                addOption = int(addOption)
            except:
                print "Invalid input."
                continue
            
            if addOption == 1:
                manualAdd = {}
                for item in terms:
                    manualAdd[item] = input("Please enter the" + item)
                    
                for item in manualAdd:
                    if item in substitutions:
                        manualAdd[substitutions[item]] = manualAdd.pop(item)
                
                manualBook = Book(manualAdd["bc"])
                manualBook.createFromDict(manualAdd)
                bookDB = Bdb(dbLocation)
                bookDB.store(manualBook)
                
            elif addOption == 2:
                isbn = input("Please enter the 10 or 13 digit ISBN: ")
                lookup = Lookup()
                bookInfo = lookup.byISBN(isbn)
                bc = ('''Please enter a unique barcode, or -1 to autogenerate: ''')
                
                try:
                    bc = int(bc)
                except:
                    print "Invalid input."
                    continue
                
                if bc == -1:
                    bookInfo["bc"] = randomBC()
                else:
                    bookInfo["bc"] = bc
                
                location = input('''Please enter the location of the book, default blank: ''')
                bookInfo["location"] = location
                
                call_num = input('''Please enter the call number of the book: ''')
                bookInfo["call_num"] = call_num
                
                tags = input('''Please enter any tags, separated by a comma: ''')
                tags = tags.strip()
                tags = tags.split(',')
                bookInfo["tags"] = tags
            
                print '''Ok, everything should be set.  I'll show you what I've got,
                and if it looks good, just press enter, otherwise type something in
                and I'll return you to the beginning.'''
                
                for item in bookInfo:
                    print str(item) + ": " + str(bookInfo[item])
                    
                isOk = input("")
                
                if isOk != "": # not 100% sure this will work
                    continue
                else:
                    addBook = Book(bookInfo["bc"])
                    addBook.createFromDict(bookInfo)
                    bookDB = Bdb(dbLocation)
                    bookDB.store(addBook)
                    
            elif addOption == 3:
                title = input("Please enter the title you'd like to search for:")
                lookup = Lookup()
                books = lookup.byTitle(title)
                count = 1
                raw_input('''The following are the results.  Please enter the number of the\n
                result you'd like.  Press any key to display them.''')
                for book in books.get('items', []):
                    print '%i) Title: %s, Authors: %s' % (
                                                          count,
                                                          book['volumeInfo']['title'],
                                                          book['volumeInfo']['authors'])
                    count += 1
                userChoice = input("Which result would you like? ")
                bookInfo = lookup.chooseResponse(books[userChoice]['id'])
                
                bc = ('''Please enter a unique barcode, or -1 to autogenerate: ''')
                
                try:
                    bc = int(bc)
                except:
                    print "Invalid input."
                    continue
                
                if bc == -1:
                    bookInfo["bc"] = randomBC()
                else:
                    bookInfo["bc"] = bc
                
                location = input('''Please enter the location of the book, default blank: ''')
                bookInfo["location"] = location
                
                call_num = input('''Please enter the call number of the book: ''')
                bookInfo["call_num"] = call_num
                
                tags = input('''Please enter any tags, separated by a comma: ''')
                tags = tags.strip()
                tags = tags.split(',')
                bookInfo["tags"] = tags
            
                print '''Ok, everything should be set.  I'll show you what I've got,
                and if it looks good, just press enter, otherwise type something in
                and I'll return you to the beginning.'''
                
                for item in bookInfo:
                    print str(item) + ": " + str(bookInfo[item])
                    
                isOk = input("")
                
                if isOk != "": # not 100% sure this will work
                    continue
                else:
                    addBook = Book(bookInfo["bc"])
                    addBook.createFromDict(bookInfo)
                    bookDB = Bdb(dbLocation)
                    bookDB.store(addBook)
                
        elif todo == 2:
            todo = input('''We're going to delete a book.  Do you have the barcode? [y/N]: ''')
            if todo.strip() == "" or todo.strip().lower() == "n":
                results = search()
                i = 1
                for item in results:
                    print(i + ") " + item) # not sure how this will come out.
                delMe = input("Which one is it? ")
                
                try:
                    delMe = int(delMe)
                except:
                    print "Invalid input."
                    continue
                
                delMe = results[delMe - 1]
                delMe = delMe.split(",")
                delMe = Book(delMe[0]) # this is really fudged atm.  serious testing needed
                theDB = Bdb(dbLocation)
                theDB.delete(delMe)
                print "Deleted."
                
            elif todo.strip().lower() == "y":
                delMe = input("Ok, enter it now: ")
                if delMe.strip() == "":
                    print "Invalid input."
                else:
                    try:
                        delMe = int(delMe)
                    except:
                        print "Invalid input."
                        continue
                    
                    delMe = Book(delMe)
                    theDB = Bdb(dbLocation)
                    theDB.delete(delMe)
                    print "Deleted."
                    
        elif todo == 3:
            results = search()
            i = 1
            for item in results:
                print str(i) + ") " + str(item)
                
        elif todo == 4:
            theDB = Bdb(dbLocation)
            for item in theDB.getAll():
                print item
                
        elif todo == 5:
            config = ConfigParser.RawConfigParser()
            config.read('.pyberry')
            loc = config.get('local', 'dbPath')
            print "Current location is %s" % loc
            changeIt = input("Would you like to change it? [y/N]: ")
            
            if changeIt.strip().lower() != 'y':
                continue
            else:
                newLoc = input(''''Please enter a new path, either relative to current directory\n
                or an absolute path.  I'll fail if there's a permissions issue, though.\n
                Current path %s''' % loc) # @todo: input checking
                
                config.set('local', 'dbPath', newLoc)
                with open('.pyberry','wb') as configFile:
                    config.write(configFile)
                    
        elif todo == 6:
            run = False
        
        else:
            print "Invalid choice"
            continue
            