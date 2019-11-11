from server import (SMTPServer, MessageHandler, MyController)
from smtplib import SMTP as Client

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

def test_MAIL(client):
    code, message = client.docmd('MAIL FROM: <example@project.com>')
    assert(str(code) == '250')

def test_RCPT(client):
    code, message = client.docmd('RCPT TO: <example@project.com>')
    assert(str(code) == '250')

def test_DATA(client):
    pass

def test_sendmail(client):
    client.sendmail('<example@project.com>', '<example2@project.com>','hello there')
    print('---------------------------------------------')

def run_tests():
    controller = MyController(MessageHandler())
    controller.start()

    client = Client(controller.hostname, controller.port)
    client.starttls()

    client2 = Client(controller.hostname, controller.port)
    client2.starttls()

    test_HELO(client)
    if test_AUTH(client):
        test_sendmail(client)

    test_HELO(client2)
    if test_AUTH(client2):
        test_sendmail(client2)

    controller.stop()
    print('tests successful')


if __name__ == '__main__':
    run_tests()
