from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as Server, syntax
import asyncio
import ssl
import subprocess
import os
from database import (Database, User)


class SMTPServer(Server):
    @syntax('PING [ignored]')
    async def smtp_PING(self, arg):
        await self.push('259 Pong')

    @syntax("AUTH USERNAME PASSWORD [ignored]")
    async def smtp_AUTH(self, arg):
        if arg is None:
            await self.push('501 Syntax: AUTH USERNAME PASSWORD [ignored]')
            return
        else:
            credentials = arg.split(' ')
            if len(credentials) is not 2:
                await self.push('501 Syntax: AUTH USERNAME PASSWORD [ignored]')
                return
            else:
                database = Database('network_project.db')
                if database.check_credentials(credentials[0], credentials[1]):
                    await self.push('253 Authentication successful')                    
                else:
                    await self.push('535 Invalid credentials')

    @syntax("REG USERNAME PASSWORD [ignored]")
    async def smtp_REG(self, arg):
        if arg is None:
            await self.push('501 Syntax: REG USERNAME PASSWORD [ignored]')
            return
        else:
            credentials = arg.split(' ')
            if len(credentials) is not 2:
                await self.push('501 Syntax: REG USERNAME PASSWORD [ignored]')
                return
            else:
                database = Database('network_project.db')
                database.add_account(credentials[0], credentials[1])
                await self.push('253 Authentication successful')

    # uses custom response code: '255 user_id'
    @syntax("GETUSER USERNAME PASSWORD")
    async def smtp_GETUSER(self, arg):
        if arg is None:
            await self.push('501 Syntax: GETUSER USERNAME PASSWORD [ignored]')
            return
        else:
            credentials = arg.split(' ')
            if len(credentials) is not 2:
                await self.push('501 Syntax: GETUSER USERNAME PASSWORD [ignored]')
                return
            else:
                database = Database('network_project.db')
                user_id = database.get_user_id(credentials[0], credentials[1])
                response = '255 ' + str(user_id)
                await self.push(response)


class SMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:')
        print(envelope.content.decode('utf8', errors='replace'))
        print('End of message\n')

        database = Database('network_project.db')
        user_id = database.get_user_id_server(envelope.rcpt_tos[0])
        if(user_id is not -1):
            database.save_email(user_id, envelope)
            return '250 Message accepted for delivery'
        else:
            return '550 No such recepient exist'

        
class MyController(Controller):
    def factory(self):
        if not os.path.exists('cert.cert') and not os.path.exists('key.key'):
            subprocess.call("openssl req -x509 -config \"C:\\Program Files (x86)\\openssl\\openssl.cnf\" -newkey rsa:4096 -keyout key.key -out cert.cert -days 365 -nodes -subj '/CN=localhost'",shell=True)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('cert.cert', 'key.key')
        return SMTPServer(self.handler, tls_context=context, require_starttls=True)


if __name__ == '__main__':
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        controller = MyController(SMTPHandler())    
        print(controller.hostname)
        print(controller.port)
        controller.start()
        input("Server started. Press Return to quit.\n")
    except KeyboardInterrupt:
        print('stopped')
        controller.stop()
        