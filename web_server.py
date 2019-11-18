from socketserver import (BaseRequestHandler, TCPServer)
from database import (Database, User)
import sys
import re

# security
import ssl
import rsa

class MyTCPServer(TCPServer):
    def __init__(self, server_address, RequestHandlerClass, cert=None, key=None, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.cert = cert
        self.key = key

    def get_request(self):
        socket, address = self.socket.accept()
        ssl_socket = ssl.wrap_socket(socket, self.key, self.cert, server_side=True)
        return (ssl_socket, address)


class TCPHandler(BaseRequestHandler):
    def handle(self):     
        #recieve user id 
        user_id = re.findall(r'\d+', str(self.request.recv(4).strip()))
        print("{} wrote:".format(self.client_address[0]))
        print('user id: ' + str(user_id[0]))

        # get emails from database
        database = Database('network_project.db')
        user_inbox = database.get_emails(user_id[0])

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

    with MyTCPServer((HOST, PORT), TCPHandler, cert='cert.cert', key='key.key') as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print('starting...')
        server.serve_forever()
