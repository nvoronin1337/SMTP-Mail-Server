from smtplib import SMTP as Client
from database import(User)
import socket
import sys

# All comments in this file are for presentation purpose only

# MAILClient class represents a client program for 
class MAILClient(Client):
    def __init__(self, hostname, port): 
        super().__init__(hostname,port)
        self.starttls()
        self.authenticated = False
        self.user = self.sign_user()
        self.inbox = ''

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
            print(str(code) + ' ' + str(message))
            return True
        else:
            print(str(code) + ' ' + str(message))
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
        code, user_id = self.docmd(getuser_command)
        return User(user_id,email,password)

    # calls web server
    def update_inbox(self):
        # change web server ip address
        HOST, PORT = 'localhost', 9999
        if(self.authenticated is True):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as web_client:
                #connect to web server
                web_client.connect((HOST,PORT))
                
                # send user id
                web_client.sendall(bytes(str(self.user.id) + '\n', 'utf-8'))

                # send inbox length
                length = int(str(web_client.recv(1024), 'utf-8'))

                # receive emails, save them as inbox
                self.inbox = str(web_client.recv(length), 'utf-8')
        else:
            print('not authenticated')
    