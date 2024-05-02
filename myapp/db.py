import sqlite3

def create_database():

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute('''CREATE TABLE tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 description TEXT,
                 project_id INTEGER,
                 FOREIGN KEY (project_id) REFERENCES project(id))''')

    c.execute('''CREATE TABLE comments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ticket_id INTEGER,
                 comment_text TEXT,
                 FOREIGN KEY (ticket_id) REFERENCES tickets(id))''')

    c.execute('''CREATE TABLE project
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT)''')

    conn.close()


create_database()
