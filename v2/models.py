import sqlite3
from datetime import datetime


class SQLStorage():
    ''' Represents a persistence layer provided using sqlite
    '''
    FILENAME = "sql_data.db"

    def __init__(self):
        ''' initiate access to the data persistence layer
        '''
        self.conn = sqlite3.connect(self.FILENAME)
        self.data_access = self.conn.cursor()
        # data_access is now a cursor object

    def get_record(self, rid):
        ''' return a single record identified by the record id
        '''
        # note unintuitive creation of single item tuple
        self.data_access.execute(
            """SELECT * from tickets WHERE ticket_id = ?;""", (rid,))
        row = self.data_access.fetchone()
        ticket = Ticket(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0])
        return ticket

    def get_all_records(self):
        ''' return all records stored in the database
        '''
        self.data_access.execute("""SELECT * from tickets;""")
        #rows = self.data_access.fetchall()
        tickets = []
        for row in self.data_access:
            tickets.append(
                Ticket(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0]))
        return tickets

    def save_record(self, record):
        ''' add a record represented by a dict with a new id
        '''
        # if it's still 0 then it's a new record, otherwise it's not
        if record.rid == 0:
            self.data_access.execute("""INSERT INTO tickets(name,student_id,date,program,study_year,accessibility,
            category,summary) VALUES (?,?,?,?,?,?,?,?)
            """, (record.name, record.student_id, record.date, record.program, record.study_year,
                  record.accessibility, record.category, record.summary))
            record.rid = self.data_access.lastrowid
        else:
            self.data_access.execute("""UPDATE tickets SET name = ?, student_id = ?, date = ?, program = ?,
            study_year = ?, accessibility = ?, category = ?, summary = ?
            WHERE ticket_id = ?""", (record.name, record.student_id, record.date, record.program, record.study_year,
                  record.accessibility, record.category, record.summary, record.rid))
        self.conn.commit()

    def get_all_sorted_records(self):
        return sorted(self.get_all_records(), key=lambda x: x.rid)

    def delete_record(self, rid):
        # note unintuitive creation of single item tuple
        # convert to int since value comes from treeview (str)
        self.data_access.execute("""DELETE FROM tickets WHERE ticket_id = ?""",
                                 (int(rid),))
        self.conn.commit()

    def cleanup(self):
        ''' call this before the app closes to ensure data integrity
        '''
        if (self.data_access):
            self.conn.commit()
            self.data_access.close()


class Ticket():
    def __init__(self, name="", student_id=0, date=datetime.now().date(), program="", study_year="", accessibility="",
                 category="", summary="", rid=0):
        self.rid = rid
        self.name = name
        self.student_id = student_id
        self.date = date
        self.program = program
        self.study_year = study_year
        self.accessibility = accessibility
        self.category = category
        self.summary = summary

    def __str__(self):
        return (f'Ticket#: {self.rid}, Student Id: {self.student_id}; Name: {self.name}, Date: {self.date}, Program: {self.program},'
                f' Study Year: {self.study_year}, Accessibility: {self.accessibility}, Category: {self.category},'
                f'Summary: {self.summary}')
