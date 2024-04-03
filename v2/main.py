import tkinter as tk
from datetime import date
from tkinter import *
from tkinter import font as tkfont
from tkinter import messagebox
from widgets import EntryField, Combo, RadiobuttonField, ScrolledTextWidget, CalendarField
import tkinter.ttk as ttk  # just for treeview
# import entry_field  # no particular good reason I did it the other way here
from models import *  # done this way to access classes just by name
import sys  # only used for flushing debug print statements


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # this is the main database access object
        # note you must run the init_db.py script before using SQLStorage
        self.data = SQLStorage()

        self.resizable(False, False)

        # set a single font to be used throughout the app
        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Student Advising Notes Repository")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for each other custom Frame class you make, you could add it to this tuple
        for F in (StarterBrowsePage, TestPage):
            page_name = F.__name__
            # last arg - send the object that accesses the db
            frame = F(parent=container, controller=self, persist=self.data)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StarterBrowsePage")

    def show_frame(self, page_name, rid=0):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        # the edit screen requires knowledge of the id of the item
        if not rid == 0:
            frame.update(rid)
        else:
            frame.update()
        # bring it to the front of the stacking order
        frame.tkraise()


class StarterBrowsePage(tk.Frame):
    ''' the Browse page must show all the items in the database and allow
    access to editing and deleting, as well as the ability to go to a screen
    to add new ones. This is the 'home' screen.
    '''

    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # TODO: Create a "SomeBrowsePage" class that will be our main browsing frame.
        #  You can check app_demo in the Prof's github from Week10 for inspiration of class' codes.
        #  This includes creating a Treeview inside this frame. This means we should have methods such as
        #  edit_selected, on_select, delete_selected, update. Do not get frightened. We can use the demo's code
        #  to write these methods.

        # Create 2 main frames (left and right)

        self.frame2 = tk.Frame(self, borderwidth=5, relief="ridge")
        self.frame2.grid(row=0, column=1, sticky=tk.NSEW)

        self.frame3 = tk.Frame(self, borderwidth=5, relief="ridge", width=500)
        self.frame3.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame1 = tk.Frame(self, borderwidth=5, relief="ridge", width=500)
        self.frame1.grid(row=0, column=0, sticky=tk.NSEW)

        # Create frame1 widgets
        self.persist = persist  # Treeview related value
        self.data = {}  # Treeview related value
        self.data['Name'] = EntryField(self.frame1, label='Name', error_message='', validate='key',
                                       validatecommand=self.validate_only_text)
        self.data['Name'].grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.data['Name'].field.bind("<FocusOut>", self.validate_name)
        # self.name_field.field.bind("<FocusOut>", self.validate_name)

        self.data['Student_ID'] = EntryField(self.frame1, label='Student ID', error_message='', validate='key',
                                             validatecommand=self.validate_only_numbers)
        self.data['Student_ID'].grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.data['Student_ID'].field.bind("<FocusOut>", self.validate_ten_digits)
        # self.id_field.field.bind("<FocusOut>", self.validate_ten_digits)

        self.data['Date'] = CalendarField(self.frame1, label='Date')
        self.data['Date'].grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        # self.cal.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.data['Program'] = Combo(self.frame1, label='Program', options=('Anthropology', 'Art', 'Biology',
                                                                            'Communication', 'Business'))
        self.data['Program'].grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        # self.program.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self.data['Study_Year'] = RadiobuttonField(self.frame1, label='Year of Study', options=['1', '2', '3',
                                                                                                '4', '4+'], initial_value='1')
        self.data['Study_Year'].grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        # self.year_of_study.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.data['Accessibility'] = RadiobuttonField(self.frame1, label='Registered with Accessibility?',
                                                      options=['Yes', 'No'], initial_value='No')
        self.data['Accessibility'].grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        # self.accessibility.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)

        self.data['Category'] = Combo(self.frame1, label='Category of Topic', options=('Registration',
                                                                                       'Finances', 'Transfer Credit',
                                                                                       'Personal Information',
                                                                                       'Petitions', 'Graduation',
                                                                                       'Exam Identification',
                                                                                       'Absence Declaration'))
        self.data['Category'].grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        # self.topic.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)

        self.data['Summary'] = ScrolledTextWidget(self.frame1, label='Summary of Question', error_message='')
        self.data['Summary'].grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
        # self.question.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

        self.submit_button = tk.Button(self.frame1, text='Submit', width=4, height=2, command=self.submit)
        self.submit_button.grid(row=8, column=0, padx=10, pady=30)

        # Create frame3 widgets
        self.edit_data = {}
        self.edit_data['Name'] = EntryField(self.frame3, label='Name', error_message='', validate='key',
                                            validatecommand=self.validate_only_text)
        self.edit_data['Name'].grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.edit_data['Name'].field.bind("<FocusOut>", self.validate_name)
        # self.edit_name_field.field.bind("<FocusOut>", self.validate_name)

        self.edit_data['Student_ID'] = EntryField(self.frame3, label='Student ID', error_message='', validate='key',
                                                  validatecommand=self.validate_only_numbers)
        self.edit_data['Student_ID'].grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.edit_data['Student_ID'].field.bind("<FocusOut>", self.validate_ten_digits)
        # self.edit_id_field.field.bind("<FocusOut>", self.validate_ten_digits)

        self.edit_data['Date'] = CalendarField(self.frame3, label='Date')
        self.edit_data['Date'].grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        # self.edit_cal.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_data['Program'] = Combo(self.frame3, label='Program', options=('Anthropology', 'Art', 'Biology',
                                                                                 'Communication', 'Business'))
        self.edit_data['Program'].grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        # self.edit_program.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_data['Study_Year'] = RadiobuttonField(self.frame3, label='Year of Study',
                                                        options=['1', '2', '3', '4', '4+'], initial_value='1')
        self.edit_data['Study_Year'].grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        # self.edit_year_of_study.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_data['Accessibility'] = RadiobuttonField(self.frame3, label='Registered with Accessibility?',
                                                           options=['Yes', 'No'], initial_value='No')
        self.edit_data['Accessibility'].grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        # self.edit_accessibility.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_data['Category'] = Combo(self.frame3, label='Category of Topic', options=('Registration',
                                                                                            'Finances', 'Transfer Credit',
                                                                                            'Personal Information',
                                                                                            'Petitions', 'Graduation',
                                                                                            'Exam Identification',
                                                                                            'Absence Declaration'))
        self.edit_data['Category'].grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        # self.edit_topic.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_data['Summary'] = ScrolledTextWidget(self.frame3, label='Summary of Question', error_message='')
        self.edit_data['Summary'].grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
        # self.edit_question.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

        self.submit_button = tk.Button(self.frame3, text='Save Changes', width=8, height=2, command=self.edit_selected)
        self.submit_button.grid(row=8, column=0, padx=5, pady=30)

        self.cancel_button = tk.Button(self.frame3, text='Back', width=4, height=2, command=self.cancel_edit)
        self.cancel_button.grid(row=8, column=1, padx=5, pady=30)


        # Create frame2 widgets
        # self.see_directory_button = tk.Button(self.frame2, text='See Directory', command=self.go_to_directory)
        # self.see_directory_button.grid(row=0, column=0, padx=10, pady=10)

        # self.see_submission_button = tk.Button(self.frame2, text='See Submission', command=self.go_to_profile)
        # self.see_submission_button.grid(row=0, column=1, padx=10, pady=10)

        self.directory_frame = tk.Frame(self.frame2, bg='yellow', width=850, height=600)
        self.directory_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
        # TREE ALPHA VERSION START
        scrollbarx = tk.Scrollbar(self.directory_frame, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(self.directory_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.directory_frame, columns=("ticket_id", "name", "date", 'program',
                                                                'study_year', 'category'),
                                 selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.heading('ticket_id', text="Ticket ID", anchor=tk.W)
        self.tree.heading('name', text="Name", anchor=tk.W)
        self.tree.heading('date', text="Date", anchor=tk.W)
        self.tree.heading('program', text="Program", anchor=tk.W)
        self.tree.heading('study_year', text="Study Year", anchor=tk.W)
        self.tree.heading('category', text="Category", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=50, width=90)
        self.tree.column('#2', stretch=tk.NO, minwidth=50, width=90)
        self.tree.column('#3', stretch=tk.NO, minwidth=50, width=90)
        self.tree.column('#4', stretch=tk.NO, minwidth=50, width=90)
        self.tree.column('#5', stretch=tk.NO, minwidth=50, width=90)
        self.tree.column('#6', stretch=tk.NO, minwidth=50, width=94)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.pack()
        self.selected = []

        # this object is the data persistence model
        self.persist = persist
        all_records = self.persist.get_all_sorted_records()
        # grab all records from db and add them to the treeview widget
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.date, record.program, record.study_year, record.category, record.summary))
        # TREE ALPHA VERSION END

        # self.profile_frame = tk.Frame(self.frame2, bg='green', width=850, height=600)
        # self.profile_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        self.edit_button = tk.Button(self.frame2, text='Edit', width=8, height=2, command=self.confirm_edit_record)
        self.edit_button.grid(row=2, column=0, pady=20)

        self.delete_button = tk.Button(self.frame2, text='Delete', width=8, height=2, command=self.delete_selected)
        self.delete_button.grid(row=2, column=1, pady=20)

        self.grid_rowconfigure(0, weight=1)  # This makes lower edge of frames touch the bottom of the screen

    # Methods for Treeview Start
    def on_select(self, event):
        ''' add the currently highlighted items to a list
        '''
        self.selected = event.widget.selection()

    def delete_selected(self):
        ''' uses the selected list to remove and delete certain records'''
        if len(self.selected) == 0:
            messagebox.showerror(title="Delete Error", message="Please select a ticket from Treeview for deleting.")
        else:
            confirm_delete = messagebox.askokcancel("Delete", "Are you sure you want to delete this record?")
            if confirm_delete:
                for idx in self.selected:
                    print(self.tree.item(idx)['values'][0])
                    record_id = self.tree.item(idx)['values'][0]
                    # remove from the db
                    self.persist.delete_record(record_id)
                    # remove from the treeview
                    self.tree.delete(idx)

    def edit_selected(self):
        self.ticket.name = self.edit_data['Name'].get()
        self.ticket.student_id = self.edit_data['Student_ID'].get()
        self.ticket.date = self.edit_data['Date'].get()
        self.ticket.program = self.edit_data['Program'].get()
        self.ticket.study_year = self.edit_data['Study_Year'].get()
        self.ticket.accessibility = self.edit_data['Accessibility'].get()
        self.ticket.category = self.edit_data['Category'].get()
        self.ticket.summary = self.edit_data['Summary'].get()
        self.persist.save_record(self.ticket)
        self.update_treeview()

    def go_to_edit(self):
        self.edit_data['Name'].error.configure(text='')
        self.edit_data['Name'].error.configure(text='')
        self.edit_data['Student_ID'].error.configure(text='')
        self.edit_data['Student_ID'].error.configure(text='')
        self.edit_data['Summary'].error.configure(text='')
        self.edit_data['Summary'].error.configure(text='')
        self.edit_data['Name'].reset()
        self.edit_data['Student_ID'].reset()
        self.edit_data['Date'].reset()
        self.edit_data['Program'].reset()
        self.edit_data['Study_Year'].reset()
        self.edit_data['Accessibility'].reset()
        self.edit_data['Category'].reset()
        self.edit_data['Summary'].reset()
        self.frame3.lift()
        idx = self.selected[0]  # use first selected item if multiple
        record_id = self.tree.item(idx)['values'][0]
        record = self.controller.data.get_record(record_id)
        self.edit_data['Name'].dataentry.set(record.name)
        self.edit_data['Student_ID'].dataentry.set(record.student_id)
        temp_date = datetime.strptime(record.date, '%m/%d/%y')
        self.edit_data['Date'].cal.selection_set(date(temp_date.year, temp_date.month, temp_date.day))
        # print(record.date)
        # print(datetime.strptime(record.date, '%m/%d/%y'))
        self.edit_data['Program'].dataentry.set(record.program)
        self.edit_data['Study_Year'].choice.set(record.study_year)
        self.edit_data['Accessibility'].choice.set(record.accessibility)
        self.edit_data['Category'].dataentry.set(record.category)
        self.edit_data['Summary'].scrolled_text.insert(tk.END, record.summary)
        self.ticket = self.persist.get_record(record_id)

    def reset(self):  # LOOK TO THIS METHOD AND ADD NECESSARY VARIABLES TO YOUR BROWSE PAGE
        ''' on every new entry, blank out the fields
        '''
        for key in self.data:
            self.data[key].reset()

    def update(self):
        self.reset()

    def submit(self):  # LOOK TO THIS METHOD AND ADD NECESSARY VARIABLES TO YOUR BROWSE PAGE
        ''' make a new ticket based on the form
        '''
        t = Ticket(name=self.data['Name'].get(),
                   student_id=self.data['Student_ID'].get(),
                   date=self.data['Date'].get(),
                   program=self.data['Program'].get(),
                   study_year=self.data['Study_Year'].get(),
                   accessibility=self.data['Accessibility'].get(),
                   category=self.data['Category'].get(),
                   summary=self.data['Summary'].get())
        self.persist.save_record(t)
        self.update_treeview()
        self.update()

    def update_treeview(self):
        ''' to refresh the treeview, delete all its rows and repopulate from the db'''
        for row in self.tree.get_children():
            self.tree.delete(row)
        all_records = self.persist.get_all_sorted_records()
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.date, record.program, record.study_year,
                record.accessibility, record.category, record.summary))
    # Methods for Treeview End

    def validate_only_text(self, text):
        # Check if input text is valid
        
        name_valid = len(text) <= 1000 and all(char.isalpha() or char.isspace() for char in text) # I used ChatGPT to learn about the all() function

        if name_valid:
            # Clear error message
            self.data['Name'].error.configure(text='')
            self.edit_data['Name'].error.configure(text='')
        else:
            # Display error message
            self.data['Name'].error.configure(text='Please only enter letters or spaces')
            self.edit_data['Name'].error.configure(text='Please only enter letters or spaces')

        return name_valid

    # This verifies if the name is correct when the user clicks away from the entry and clears error messages accordingly
    def validate_name(self, event):
        if all(char.isalpha() or char.isspace() for char in event.widget.get()): # I used ChatGPT to learn about the event.widget.get() method
            self.data['Name'].error.configure(text='')
            self.edit_data['Name'].error.configure(text='')
        else:
            self.data['Name'].error.configure(text='Please only enter letters or spaces')
            self.edit_data['Name'].error.configure(text='Please only enter letters or spaces')

    def validate_only_numbers(self, text):
        # Check if input text is valid
        id_valid = len(text)<=10 and all(char.isdigit() for char in text)

        if id_valid:
            # Clear error message
            self.data['Student_ID'].error.configure(text='')
            self.edit_data['Student_ID'].error.configure(text='')
        else:
            # Display error message
            self.data['Student_ID'].error.configure(text='Please enter the ten digits only composed of numbers')
            self.edit_data['Student_ID'].error.configure(text='Please enter the ten digits only composed of numbers')

        return id_valid

    def validate_ten_digits(self, event):
        if len(event.widget.get()) != 10:
            self.data['Student_ID'].error.configure(text='The Student ID must be 10 digits long')
            self.edit_data['Student_ID'].error.configure(text='The Student ID must be 10 digits long')
        elif len(event.widget.get()) == 10:
            self.data['Student_ID'].error.configure(text='')
            self.edit_data['Student_ID'].error.configure(text='')

    # def go_to_directory(self):
        # self.directory_frame.lift()

    # def go_to_profile(self):
        # self.profile_frame.lift()

    def back_to_submit(self):
        self.data['Name'].error.configure(text='')
        self.edit_data['Name'].error.configure(text='')
        self.data['Student_ID'].error.configure(text='')
        self.edit_data['Student_ID'].error.configure(text='')
        self.data['Summary'].error.configure(text='')
        self.edit_data['Summary'].error.configure(text='')
        self.frame1.lift()

    def confirm_edit_record(self):
        if len(self.selected) == 0:
            messagebox.showerror(title="Select Error", message="Please select a ticket from Treeview for editing.")
        else:
            confirm_edit = messagebox.askokcancel("Edit",
                                                  "Are you sure you want to edit this record? Any data yet to be submitted or saved will be lost.")
            if confirm_edit:
                self.go_to_edit()

    def cancel_edit(self):
        confirm_cancel = messagebox.askokcancel("Cancel", "Are you sure you want to cancel your edit? Any unsaved data will be lost.")
        if confirm_cancel:
            self.back_to_submit()


class TestPage(tk.Frame):
    ''' the Browse page must show all the items in the database and allow
    access to editing and deleting, as well as the ability to go to a screen
    to add new ones. This is the 'home' screen.
    '''

    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.test_label = tk.Label(self, text="something")
        self.test_label.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
