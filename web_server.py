from socketserver import (BaseRequestHandler, TCPServer)
from database import (Database, User)
import sys
import re

class TCPHandler(BaseRequestHandler):
    def handle(self):
        
        #recieve user id 
        user_id = re.findall(r'\d+', str(self.request.recv(4).strip()))
        print("{} wrote:".format(self.client_address[0]))
        print('user id: ' + str(user_id[0]))

        # get emails from database
        database = Database('network_project.db')
        user_inbox = database.get_emails(user_id[0])
        print(user_inbox)

        # send inbox length
        length = sys.getsizeof(str(user_inbox))
        self.request.sendall(bytes(str(length) + '\n', 'utf-8'))
        print("{} sent to:".format(self.client_address[0]))
        print('length: ' + str(length))

        # send inbox
        self.request.sendall(bytes(str(user_inbox) + '\n', 'utf-8'))
        print("{} sent to:".format(self.client_address[0]))
        print('user inbox: ' + str(user_inbox))


if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    with TCPServer((HOST, PORT), TCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print('starting...')
        server.serve_forever()
