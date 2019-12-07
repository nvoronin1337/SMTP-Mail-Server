## Secure mail system in python3 with PyQt5 GUI.

1.	Graphical UI for the client (PyQt5)
2.	Client Wrapper Class (smtplib and TCP client socket)
3.	SMTP Server Wrapper Class (aiosmtp)
4.	Web Server Wrapper Class (TCP server socket)
5.  Database Wrapper Class (sqlite3)

### Flow Diagram
![flow_diagram](https://user-images.githubusercontent.com/23469990/70381942-4fb37e80-1921-11ea-97be-923fdc494f03.png)

### Graphical User Interface
The Graphical User Interface is built using python PyQt5 framework. It consists of three windows and a few dialogs (smaller windows). When app is opened by the user, the login dialog is opened. If user enters correct credentials, he is forwarded to the inbox window, else, he is shown a warning saying that his credentials are incorrect. In the inbox window, the user can input how many latest emails he wishes to see and can then see those emails as records in the table in the middle of the window. To see the message part of the email, user must select a record that he wishes to view. The record is then opened in a separate dialog and expanded to show the message part. There are also options in the menu at the top of the window. Those options allow user to navigate between his inbox and another window which allows user to wright and send emails, as well as open the project source code, or this document. There is also an incomplete option to view the outbox (sent mail).

### Client
The Client (MAILClient) is a class which inherits from smtplib.SMTP and represents a smtp client instance. Every time a new instance is being initialized, a starttls() command is called, otherwise, SMTP server will not accept connection. Besides having a default functionality of smtplib.SMTP, this class also implements other methods for sending following commands to the SMTP Server: (authenticate user, register user, get user’s id from database). Besides, this class has a method update_inbox() which opens an SSL connection with the web server and after some information exchange updates this client’s inbox.

### SMTP Server
The SMTPServer consists of several classes: (server, handler, and controller). Server and controller inherit from aiosmtpd.smtp.SMTP and aiosmtpd.controller.Controller accordingly. The server class is used to add custom commands which our server can process: (PING, AUTH, REG, GETUSER). Each of these methods are asynchronous and return some smtp response when finished. Handler class is used to override how the DATA command is being processed by the server. I’ve changed it so every email is being saved in the database unless the email address of the recipient doesn’t belong to the domain ‘@project.com’ in which case a smtp response ‘550 no such recipient exists is returned’. The controller class is responsible for setting up the SSL context for the SMTP server and creating/running the server instance asynchronously.

### Web Server
The Web Server consists of two classes: server itself, and a handler. Server class inherits from the socketserver.TCPServer. SSL key and certificate are added as parameters to the server’s initializer. Also, get_request() method is overridden so it can create a new SSL secured socket to communicate with the client. Handler is used to receive, parse, and process requests from user and to send responses.

### Database
Database consists of two models (tables): user, and email. I use sqlite as a database engine. It is assumed that the smtp server and web server use the same database, so both servers must run on the same machine.

### Workflow
As can be seen on the diagram above, when server handles DATA command (in other words when client has attempted to send an email to someone), server can process it but can’t redirect it to another user. That is due to how the SMTP protocol designed. In real world, SMTP used for sending emails, and POP3 used for receiving them. In my case, I’ve decided to implement a similar idea but with the use of HTTP instead of POP3 due to a lot of complications that I have faced during the research on implementing a POP3 server. In my case, server saves email with a foreign key to the recipient. Then, when recipient logs in and decides to check his inbox, client sends its account id to the web server and receives his inbox.
