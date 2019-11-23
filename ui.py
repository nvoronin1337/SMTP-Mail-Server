from client import MAILClient
from smtplib import SMTPException
from enum import IntEnum
import ast


class MenuChoice(IntEnum):
    INBOX = 1
    NEW_MAIL = 2
    QUIT = 3


if __name__ == '__main__':
    # change SMTP server ip address
    HOST, PORT = '::1', 8025
    email = input('Enter Email: ')
    password = input('Enter Password: ')
    is_registered = input('Are you already registered for this account? 1/0: ')
    client = MAILClient(HOST, PORT, email, password, is_registered)
    print('\nWelcome ' + str(client.user.email) + '!' )
    running = True
    while(running):
        print('1. Check inbox.')
        print('2. New mail.')
        print('3. Quit.')
        choice = MenuChoice(int(input('=>')))
        if(choice is MenuChoice.INBOX):
            client.update_inbox()
            print('\nYour inbox:')
            parsed = ast.literal_eval(client.inbox)
            for email in parsed:
                print(email)
            print()
        elif(choice is MenuChoice.NEW_MAIL):
            rcpt_to = input('\nTo: ')
            message = input('Message: ')
            try:
                client.sendmail(client.user.email, rcpt_to, message)
            except SMTPException:
                print('Error. No such recipient exists on this domain.')
            print()
        elif(choice is MenuChoice.QUIT):
            print('Bye ' + str(client.user.email) + '!')
            client.quit()
            running = False
        else:
            print('Please select a valid action. (Enter 1,2, or 3)\n')
