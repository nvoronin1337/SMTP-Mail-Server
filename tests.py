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
    code, message = client.docmd('MAIL FROM: <asdaskek@project.com>')
    assert(str(code) == '250')
    code, message = client.docmd('MAIL FROM: <asdaskek@wrong.com>')
    assert(str(code) == '551')


def test_RCPT(client):
    code, message = client.docmd('RCPT TO: kek@project.com')
    assert(str(code) == '250')


def run_tests():
    controller = MyController(Sink())
    controller.start()
    client = Client(controller.hostname, controller.port)

    test_HELO(client)
    test_PING(client)
    test_AUTH(client)
    test_MAIL(client)
    #test_RCPT(client)

    controller.stop()
    print('tests successful')


if __name__ == '__main__':
    run_tests()
