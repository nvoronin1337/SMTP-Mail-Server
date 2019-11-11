from aiosmtpd.controller import Controller
import asyncio
from aiosmtpd.smtp import SMTP as Server, syntax
import ssl
import subprocess
import os

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
                if credentials[0] == 'username' and credentials[1] == 'password':
                    self.authenticated = True
                    await self.push('253 Authentication successful')
                else:
                    await self.push('535 Invalid credentials')

    @syntax('MAIL FROM: <address@project.com>')
    async def smtp_MAIL(self, arg):
        if(arg is None):
            await self.push('501 Syntax: MAIL FROM: <address@example.com>')
        else:
            if(arg[7:len(arg)-1].endswith('@project.com')):
                self.envelope.mail_from = arg[7:len(arg)-1]
                message = '250 OK MAIL FROM: ' + arg[7:len(arg)-1]
                await self.push(message)
            else:
                await self.push('551 not relaying to that domain')
                
    @syntax('RCPT TO: <address@project.com')
    async def smtp_RCPT(self, arg):
        if arg is None:
            await self.push('501 Syntax: RCPT TO: <address@example.com>')
        else:
            self.envelope.rcpt_tos = arg[5:len(arg)-1]
            message = '250 OK RCPT TO: ' + arg[5:len(arg)-1]
            await self.push(message)

    
class MyController(Controller):
    def factory(self):
        if not os.path.exists('cert.cert') and not os.path.exists('key.key'):
            subprocess.call("openssl req -x509 -config \"C:\\Program Files (x86)\\openssl\\openssl.cnf\" -newkey rsa:4096 -keyout key.key -out cert.cert -days 365 -nodes -subj '/CN=localhost'",shell=True)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('cert.cert', 'key.key')
        return SMTPServer(self.handler, tls_context=context, require_starttls=True)
