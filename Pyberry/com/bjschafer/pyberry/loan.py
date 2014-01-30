'''
Created on Oct 18, 2013

@author: braxton
'''


class Loan(object):
    """
    Would it be a better idea to have the book and person as their objects?
    Also the dates...datetime objects?
    """

    def __init__(self, uid, book=0, person=0, issue_date='', due_date='', is_historical=False):

        self.uid = uid
        self.book = book
        self.person = person
        self.issue_date = issue_date
        self.due_date = due_date
        self.is_historical = is_historical
        
    def edit(self, uid=None, book=None, person=None, issue_date=None, due_date=None, is_historical=None):
        if uid is not None:
            self.uid = uid
        if book is not None:
            self.book = book
        if person is not None:
            self.person = person
        if issue_date is not None:
            self.issue_date = issue_date
        if due_date is not None:
            self.due_date = due_date
        if is_historical is not None:
            self.is_historical = is_historical
            
    def get_list_representation(self):
        return [self.uid, self.book, self.person, self.issue_date, self.due_date, self.is_historical]
    
    def create_from_list(self, my_list):
        if len(my_list) != 6:
            raise ValueError("Incorrect list length")
        else:
            self.uid = my_list[0]
            self.book = my_list[1]
            self.person = my_list[2]
            self.issue_date = my_list[3]
            self.due_date = my_list[4]
            self.is_historical = my_list[5]