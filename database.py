import sqlite3


class User:
    def __init__(self, email, password):
        self.id = None
        self.email = email
        self.password = password


class Email:
    def __init__(self, mailfrom, rcpttos, data,):
        self.mailfrom = mailfrom
        self.rcpttos = rcpttos
        self.message = data


class Database:
    def __init__(self, user, database):
        self.user = user
        self.database = database
    
    def init_db(self):
        query_create_accounts = """create table if not exists accounts (id integer PRIMARY KEY AUTOINCREMENT,
                                    email text not null, password text not null);"""

        query_create_emails = """create table if not exists emails (id integer PRIMARY key AUTOINCREMENT,
                                   acc_id integer not null,
                                   mail_from text not null,
                                   rcpt_tos text,
                                   message text,
                                   time_received text,
                                   FOREIGN key (acc_id) REFERENCES ACCOUNTS(id));"""

        with sqlite3.connect(self.database) as connection:
            cursorObj = connection.cursor()
            cursorObj.execute(query_create_accounts)
            connection.commit()
            cursorObj.execute(query_create_emails)
            connection.commit()

    def check_credentials(self):
        with sqlite3.connect(self.database) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT id FROM accounts WHERE email = ?",(self.user.email,))
            record = cursor.fetchone()
            if(record is None):
                return False
            else:
                self.user.id = record[0]
                return True

    def add_account(self):
        with sqlite3.connect(self.database) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO accounts(email,password) values(?,?)", (self.user.email, self.user.password))

    def save_email(self, email):
        with sqlite3.connect(self.database) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO emails values(?,?,?,?,?)")
            