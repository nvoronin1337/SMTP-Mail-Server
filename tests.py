from server import (SMTPServer, SMTPHandler, MyController)
from client import SMTPClient as Client

def test_HELO(client):
    code, message = client.helo('host1')
    assert(str(code) == '250')

def test_PING(client):
    code, message = client.docmd('PING')
    assert(str(code) == '259')

def test_AUTH(client):
    code, message = client.docmd('AUTH username password')
    assert(str(code) == '253')
    return True

def test_DATA(client):
    pass

def test_sendmail(client):
    client.sendmail(client.user.email, '<example2@project.com>','hello there')
    print('---------------------------------------------')

def run_tests():
    controller = MyController(SMTPHandler())
    controller.start()

    client = Client(controller.hostname, controller.port)
    
    test_HELO(client)
    test_sendmail(client)

    controller.stop()
    print('tests successful')


if __name__ == '__main__':
    run_tests()
