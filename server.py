from aiosmtpd.controller import Controller
import asyncio
from aiosmtpd.smtp import SMTP as Server, syntax


class SMTPServer(Server):
    @syntax('PING [ignored]')
    async def smtp_PING(self, arg):
        await self.push('259 Pong')

    @syntax("AUTH USERNAME PASSWORD")
    async def smtp_AUTH(self, arg):
        if arg is None:
            await self.push('501 Syntax: AUTH USERNAME')
            return
        else:
            credentials = arg.split(' ')
            if len(credentials) is not 2:
                await self.push('501 Syntax: AUTH USERNAME')
                return
            else:
                #check if data is in db
                if credentials[0] == 'username' and credentials[1] == 'password':
                    self.authenticated = True
                    await self.push('253 Authentication successful')
                else:
                    await self.push('535 Invalid credentials')

    @syntax('MAIL FROM: <address@example.com>')
    async def smtp_MAIL(self, arg):
        if(arg is None):
            await self.push('501 Syntax: MAIL FROM: <address@example.com>')
        else:
            if(arg[7:len(arg)-1].endswith('@project.com')):
                await self.push('250 OK')
            else:
                await self.push('551 not relaying to that domain')

    
class MyController(Controller):
    def factory(self):
        return SMTPServer(self.handler)
