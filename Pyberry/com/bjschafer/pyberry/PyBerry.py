import random
from com.bjschafer.pyberry.lookup import Lookup
from com.bjschafer.pyberry.book import Book
from com.bjschafer.pyberry.bdb import Bdb

DB_location = "/tmp/example"
terms = ["title", "author", "barcode", "isbn", "number of pages", "publication year",
         "location", "description", "call number", "tags"]
substitutions = {"barcode": "bc", "number of pages": "pages", "publication year": "publ_year",
                 "call number": "call_num"}

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
    print("Welcome to searching!")
    print('''You can search by: title, author, barcode, isbn, number of pages, publication year,
    location, description, call number, or tags.''')
    search_field = input("Which would you like to search by? ")
    search_term = input("OK, go ahead: ")
    
    if search_field not in terms:
        print("Error, exiting.")
        pass
    elif search_term == "":
        print("Error, exiting.")
        pass
    else:
        if search_field in substitutions:
            search_field = substitutions[search_field]
        theDB = Bdb(DB_location)
        return theDB.search(search_field, search_term)
            
    

if __name__ == '__main__':
    run = True
    
    # logo
    print('''
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
                                 77777777I??7     ''')
    print("Welcome to PyBerry!")
    
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
            print("Invalid input.")
            pass
        
        if todo < 1 or todo > 6:
            print("Invalid input.")
            pass
        
        if todo == 1:
            addIt = input('''Let's add a book.  How would you like to add it?\n
            1) Manually\n
            2) Search by ISBN: ''')
            
            try:
                addIt = int(addIt)
            except:
                print("Invalid input.")
                pass
            
            if addIt == 1:
                manual = {}
                for item in terms:
                    manual[item] = input("Please enter the " + item)
                    
                for item in manual:
                    if item in substitutions:
                        manual[substitutions[item]] = manual.pop(item)
                        
                yourBook = Book(manual["bc"])
                yourBook.createFromDict(manual)
                theDB = Bdb(DB_location)
                theDB.store(yourBook)
            
            elif addIt == 2:
                isbn = input("Please enter the 10 or 13 digit ISBN: ")
                lookup = Lookup()
                information = lookup.byISBN(isbn)
                bc = ('''Please enter a unique barcode, or -1 to autogenerate: ''')
                
                try:
                    bc = int(addIt)
                except:
                    print("Invalid input.")
                    pass
                
                if bc == -1:
                    information["bc"] = randomBC
                else:
                    information["bc"] = bc
                    
                loc = input('''Please enter the location of the book, default blank: ''')
                information["location"] = loc
                
                call_num = input('''Please enter the call number of the book: ''')
                information["call_num"] = call_num
                
                tags = input('''Please enter any tags, separated by a comma: ''')
                tags = tags.strip()
                tags = tags.split(',')
                information["tags"] = tags
                
                print('''Ok, everything should be set.  I'll show you what I've got,
                and if it looks good, just press enter, otherwise type something in
                and I'll return you to the beginning.''') 
                
                for item in information:
                    print(str(item) + ": " + str(information[item]))
                    
                good = input("")
                
                if good != "": # not 100% sure this'll work.
                    pass
                else:
                    yourBook = Book(information["bc"])
                    yourBook.createFromDict(information)
                    theDB = Bdb(DB_location)
                    theDB.store(yourBook)
                    
            else:
                print("Invalid input.")
                pass
            
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
                    print("Invalid input.")
                    pass
                
                delMe = results[delMe - 1]
                delMe = delMe.split(",")
                delMe = Book(delMe[0]) # this is really fudged atm.  serious testing needed
                theDB = Bdb(DB_location)
                theDB.delete(delMe)
                print("Deleted.")
                
            elif todo.strip().lower() == "y":
                delMe = input("Ok, enter it now: ")
                if delMe.strip() == "":
                    print("Invalid input.")
                else:
                    try:
                        delMe = int(delMe)
                    except:
                        print("Invalid input.")
                        pass
                    
                    delMe = Book(delMe)
                    theDB = Bdb(DB_location)
                    theDB.delete(delMe)
                    print("Deleted.")
                    
        elif todo == 3:
            results = search()
            i = 1
            for item in results:
                print(str(i) + ") " + str(item))
                
        elif todo == 4:
            theDB = Bdb(DB_location)
            for item in theDB.getAll():
                print(item)
        
        elif todo == 5: # not sure about the scoping of this.
            # TODO: need input checking on this.
            DB_location = input("Enter a new database location: ")
            
        elif todo == 6:
            run = False
                