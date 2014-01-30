
class Person(object):

    def __init__(self, uid, first_name='', last_name='', email='', phone_num='', address='', city='', state='', notes=''):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_num = phone_num
        self.address = address
        self.city = city
        self.state = state
        self.notes = notes
        
    def edit(self, uid=None, first_name=None, last_name=None, email=None, phone_num=None, address=None, city=None, state=None, notes=None):
        if uid is not None:
            self.uid = uid
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        if phone_num is not None:
            self.phone_num = phone_num
        if address is not None:
            self.address = address
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state
        if notes is not None:
            self.notes = notes
            
    def get_list_representation(self):
        return [self.uid, self.first_name, self.last_name, self.email, self.phone_num,
                self.address, self.city, self.state, self.notes]
        
    def create_from_list(self, my_list):
        if len(my_list) != 9:
            raise ValueError("Incorrect list length")
        else:
            self.uid = my_list[0]
            self.first_name = my_list[1]
            self.last_name = my_list[2]
            self.email = my_list[3]
            self.phone_num = my_list[4]
            self.address = my_list[5]
            self.city = my_list[6]
            self.state = my_list[7]
            self.notes = my_list[8]