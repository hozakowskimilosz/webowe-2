
import uuid 

class Session:
    session = []
    id = uuid.uuid1()

    def __init__(self):
        print("Session cache initialized")

    def add_user(self, username):
        self.session.append(username)
        
    def contains_user(self, username):
        if username in self.session:
            return True
        return False
        

        