import sqlite3


def connect_database():
    global conn, cur

    # will connect to db if exists, or create a new one.
    conn = sqlite3.connect('sql_data.db')

    cur = conn.cursor()


def create_database():
    cur.execute('''DROP TABLE IF EXISTS tickets;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "tickets" (
            "ticket_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL CHECK (name != ''),
            "student_id" INTEGER NOT NULL CHECK (length(student_id) = 10),
            "date" DATE NOT NULL CHECK (date != ''),
            "program" TEXT NOT NULL CHECK (program != ''),
            "study_year" TEXT NOT NULL CHECK (study_year != ''),
            "accessibility" TEXT NOT NULL CHECK (accessibility != ''),
            "category" TEXT NOT NULL CHECK (category != ''),
            "summary" TEXT NOT NULL CHECK (summary != '')
            );''')
    # cur.execute('''CREATE TABLE IF NOT EXISTS "tickets" (
    #         "ticket_id"	INTEGER PRIMARY KEY,
    #         "name"	TEXT NOT NULL,
    #         "student_id" INTEGER NOT NULL,
    #         "date"	DATE NOT NULL,
    #         "program" TEXT NOT NULL,
    #         "study_year" TEXT NOT NULL,
    #         "accessibility" TEXT NOT NULL,
    #         "category"	TEXT NOT NULL,
    #         "summary" TEXT NOT NULL
    #         );''')
    # check lecture slides from week 11 to insert already existing data by cur.execute
    # Manually inserting data
    cur.executescript("""
    INSERT INTO tickets (ticket_id, name, student_id, date, program, study_year, accessibility, category, summary)
     VALUES (1, 'Rudolf Adler', '1004567890', '02/10/05', 'Communication', '2', 'No', 'Finances', 'Something happened');
    """)


def close_database():
    conn.commit()
    conn.close()


if __name__ == '__main__':
    connect_database()
    create_database()
    close_database()
