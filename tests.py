from server import (SMTPServer, MyController)
from smtplib import SMTP as Client
from aiosmtpd.handlers import Sink


def test_HELO(client):
    code, message = client.helo('host1')
    assert(str(code) == '250')

def test_PING(client):
    code, message = client.docmd('PING')
    assert(str(code) == '259')

def test_AUTH(client):
    code, message = client.docmd('AUTH username password')
    assert(str(code) == '253')

def test_MAIL(client):
    code, message = client.docmd('MAIL FROM: <example@project.com>')
    assert(str(code) == '250')

def test_RCPT(client):
    code, message = client.docmd('RCPT TO: <example@project.com>')
    assert(str(code) == '250')

def test_DATA(client):
    pass

def test_sendmail(client):
    client.sendmail('example@project.com', 'example2@project.com','hello there')
    print('---------------------------------------------')

def run_tests():
    controller = MyController(Sink())
    controller.start()

    client = Client(controller.hostname, controller.port)
    client.starttls()
    client.set_debuglevel(True)

    test_HELO(client)
    test_PING(client)
    test_AUTH(client)
    test_sendmail(client)
    print('client 1 end')

    client2 = Client(controller.hostname, controller.port)
    client2.starttls()
    client2.set_debuglevel(True)

    test_HELO(client2)
    test_PING(client2)
    test_AUTH(client2)
    test_sendmail(client2)
    print('client 2 end')

    controller.stop()
    print('tests successful')


if __name__ == '__main__':
    run_tests()
