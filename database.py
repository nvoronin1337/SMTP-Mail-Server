import sqlite3
import datetime

query_create_accounts = """create table if not exists accounts (id integer PRIMARY KEY AUTOINCREMENT,
                                    email text not null, password text not null);"""

query_create_emails = """create table if not exists emails (id integer PRIMARY key AUTOINCREMENT,
                                   acc_id integer not null,
                                   mail_from text not null,
                                   rcpt_tos text,
                                   message text,
                                   time_received text,
                                   FOREIGN key (acc_id) REFERENCES ACCOUNTS(id));"""


class User:
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


class Email:
    def __init__(self, id, mailfrom, rcpttos, data, time_received):
        self.acc_id = id
        self.mailfrom = mailfrom
        self.rcpt_tos = rcpttos
        self.message = data
        self.time_received = time_received


class Database:
    def __init__(self, name):
        self.name = name
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.name) as db_connection:
            cursorObj = db_connection.cursor()
            cursorObj.execute(query_create_accounts)
            db_connection.commit()
            cursorObj.execute(query_create_emails)
            db_connection.commit()

    def get_user_id(self, email, password):
         with sqlite3.connect(self.name) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT id FROM accounts WHERE email = ? AND password = ?", (email, password))
            record = cursor.fetchone()
            if(record is None):
                return -1
            else:
                return int(record[0])

    def get_user_id_server(self, email):
        with sqlite3.connect(self.name) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT id FROM accounts WHERE email = ?", (email,))
            record = cursor.fetchone()
            if(record is None):
                return -1
            else:
                return int(record[0])

    def check_credentials(self, email, password):
        with sqlite3.connect(self.name) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT id FROM accounts WHERE email = ? AND password = ?", (email, password))
            record = cursor.fetchone()
            if(record is None):
                return False
            else:
                return True

    def add_account(self, email, password):
        with sqlite3.connect(self.name) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO accounts(email,password) values(?,?)", (email, password))
            db_connection.commit()


    def save_email(self, user_id, envelope):
        with sqlite3.connect(self.name) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO emails(acc_id, mail_from, rcpt_tos, message, time_received) values(?,?,?,?,?)", (user_id, envelope.mail_from, str(envelope.rcpt_tos[0]), envelope.content.decode('utf8', errors='replace'), datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")))

    def get_emails(self, user_id, limit=None):
        with sqlite3.connect(self.name) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT mail_from, message, time_received FROM emails where acc_id = ? order by time_received desc;", [user_id])
            records = cursor.fetchall()
            return records