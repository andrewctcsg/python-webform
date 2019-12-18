data1 = []
class Form:
    def __init__(self, name, last_name, email, mobile):
        self.first_name = name
        self.last_name = last_name
        self.email = email
        self.mobile_number = mobile

        data1.append(self)

    def databasepacking(self):
        return {"first_name": self.first_name, "last_name": self.last_name, "_id": self.email, "mobile": self.mobile_number}
