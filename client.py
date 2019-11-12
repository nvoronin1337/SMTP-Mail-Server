from smtplib import SMTP as Client
from database import(User)


class SMTPClient(Client):
    def __init__(self, hostname, port): 
        super().__init__(hostname,port)
        self.starttls()
        self.authenticated = False
        self.user = self.sign_user()
        self.inbox = None

    def sign_user(self):
        while(not self.authenticated):
            email = input('Email: ')
            password = input('Password: ')
            if self.login(email,password):
                self.authenticated = True
                return self.get_user(email, password)
            else:
                is_register = input('Do you want to register with these credentials? y/n: ')
                if(is_register == 'y' or is_register == 'Y'):
                    if self.register(email, password) is True:
                        self.authenticated = True
                        return self.get_user(email, password)
                    else:
                        print('Unexpected error.')
                else:
                    print("Can't sign in.")

    def login(self, email, password):
        auth_command = 'AUTH ' + str(email) + ' ' + str(password)
        code, message = self.docmd(auth_command)
        if(str(code) == '253'):
            print(code)
            print(message)
            return True
        else:
            print(code)
            print(message)
            return False
    
    def register(self, email, password):
        reg_command = 'REG ' + str(email) + ' ' + str(password)
        code, message = self.docmd(reg_command)
        if(str(code) == '253'):
            print(message)
            return True
        else:
            print(message)
            return False

    def get_user(self, email, password):
        getuser_command = 'GETUSER ' + str(email) + ' ' + str(password)
        code, message = self.docmd(getuser_command)
        if(str(code) == '255'):
            print('Received user: ' + str(message) + ' ' + str(email) + ' ' + str(password))
        return User(message,email,password)
