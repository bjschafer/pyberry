'''
Created on Dec 1, 2012

@author: braxton
'''
import random
from com.bjschafer.pyberry.lookup import Lookup
from com.bjschafer.pyberry.book import Book
from com.bjschafer.pyberry.bdb import Bdb

def randomBC():
    '''
    This probably isn't elegant, but it should give random numbers
    that are rather not likely to collide.'''
    gen = random()
    temp = gen.randrange(100000,999999)
    return abs(temp+gen.randrange(100000,999999))
    

if __name__ == '__main__':
    run = True
    print("Welcome to PyBerry!")
    
    while run:
        toDo = input('''What would you like to do?  Your choices are:\n
        1) Add a book\n
        2) Delete a book\n
        3) Search for a book\n
        4) Show all books: ''') # currently only 1) Add a book is implemented in the UI.
        #2) Delete a book and 3) Search for a book require some backend code to become
        #functional.
        # @todo: Write options 2 & 3
        
        try:
            toDo = int(toDo)
        except:
            print("Invalid input.")
            pass
        
        if toDo < 1 or toDo > 4:
            print("Invalid input.")
            pass
        
        if toDo == 1:
            addIt = input('''Let's add a book.  How would you like to add it?\n
            1) Manually\n
            2) Search by ISBN: ''')
            # I was too lazy when I wrote this to write the manual add option.  It'll
            # be added later.
            # @todo: Write manual option.
            
            try:
                addIt = int(addIt)
            except:
                print("Invalid input.")
                pass
            
            if addIt == 1:
                pass
            
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
                tags.trim()
                tags = tags.split(',')
                information["tags"] = tags
                
                print('''Ok, everything should be set.  I'll show you what I've got,
                and if it looks good, just press enter, otherwise type something in
                and I'll return you to the beginning.''') # I should change how this
                # does business someday.  It's not elegant and user-friendly as it just
                # raw prints the dictionary.  Functional, but not elegant.
                # @todo: Elegant output here.
                
                good = input(information)
                
                if good != "": # not 100% sure this'll work.
                    pass
                else:
                    yourBook = Book(information["bc"])
                    yourBook.createFromDict(information)
                    theDB = Bdb("/tmp/example")
                    theDB.store(yourBook)
                    
            else:
                print("Invalid input.")
                pass