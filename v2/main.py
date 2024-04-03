import tkinter as tk
from datetime import date
from tkinter import *
from tkinter import font as tkfont
from tkinter import messagebox
from new_widgets import EntryField, Combo, RadiobuttonField, ScrolledTextWidget, CalendarField
import tkinter.ttk as ttk  # just for treeview
# import entry_field  # no particular good reason I did it the other way here
from new_models import *  # done this way to access classes just by name
import sys  # only used for flushing debug print statements


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # this is the main database access object
        # note you must run the init_db.py script before using SQLStorage
        self.data = SQLStorage()

        self.resizable(True, True)

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
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)

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

        # Create 3 main frames (left (submit_frame and edit_frame) and right (treeview_frame and directory_frame))

        self.treeview_frame = tk.Frame(self, borderwidth=5, relief="ridge")
        self.treeview_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_rowconfigure(1, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=1)
        self.treeview_frame.grid_columnconfigure(1, weight=1)

        self.edit_frame = tk.Frame(self, borderwidth=5, relief="ridge")
        self.edit_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.edit_frame.grid_rowconfigure(0, weight=1)
        self.edit_frame.grid_columnconfigure(0, weight=1)

        self.submit_frame = tk.Frame(self, borderwidth=5, relief="ridge")
        self.submit_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.submit_frame.grid_rowconfigure(0, weight=1)
        self.submit_frame.grid_rowconfigure(1, weight=1)
        self.submit_frame.grid_rowconfigure(2, weight=1)
        self.submit_frame.grid_rowconfigure(3, weight=1)
        self.submit_frame.grid_rowconfigure(4, weight=1)
        self.submit_frame.grid_rowconfigure(5, weight=1)
        self.submit_frame.grid_rowconfigure(6, weight=1)
        self.submit_frame.grid_rowconfigure(7, weight=1)
        self.submit_frame.grid_columnconfigure(0, weight=1)
        self.submit_frame.grid_columnconfigure(1, weight=1)

        # Create submit_frame widgets
        self.persist = persist  # Treeview related value
        self.data = {}  # Treeview related value
        self.data['Name'] = EntryField(self.submit_frame, label='Name', error_message='', validate='key',
                                       validatecommand=self.validate_only_text)
        self.data['Name'].grid(row=0, column=0, sticky=tk.W, padx=10, pady=2)
        self.data['Name'].field.bind("<FocusOut>", self.validate_name)
        

        self.data['Student_ID'] = EntryField(self.submit_frame, label='Student ID', error_message='', validate='key',
                                             validatecommand=self.validate_only_numbers)
        self.data['Student_ID'].grid(row=1, column=0, sticky=tk.W, padx=10, pady=2)
        self.data['Student_ID'].field.bind("<FocusOut>", self.validate_ten_digits)
        

        self.data['Date'] = CalendarField(self.submit_frame, label='Date')
        self.data['Date'].grid(row=2, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.data['Program'] = Combo(self.submit_frame, label='Program', options=('Anthropology', 'Art', 'Biology',
                                                                            'Communication', 'Business'))
        self.data['Program'].grid(row=3, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.data['Study_Year'] = RadiobuttonField(self.submit_frame, label='Year of Study', options=['1', '2', '3',
                                                                                                '4', '4+'], initial_value='1')
        self.data['Study_Year'].grid(row=4, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.data['Accessibility'] = RadiobuttonField(self.submit_frame, label='Registered with Accessibility?',
                                                      options=['Yes', 'No'], initial_value='No')
        self.data['Accessibility'].grid(row=5, column=0, sticky=tk.W, padx=10, pady=2)


        self.data['Category'] = Combo(self.submit_frame, label='Category of Topic', options=('Registration',
                                                                                       'Finances', 'Transfer Credit',
                                                                                       'Personal Information',
                                                                                       'Petitions', 'Graduation',
                                                                                       'Exam Identification',
                                                                                       'Absence Declaration'))
        self.data['Category'].grid(row=6, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.data['Summary'] = ScrolledTextWidget(self.submit_frame, label='Summary of Question', error_message='')
        self.data['Summary'].grid(row=7, column=0, sticky=tk.W, padx=10, pady=2)


        self.submit_button = tk.Button(self.submit_frame, text='Submit', width=8, height=2, command=self.submit)
        self.submit_button.grid(row=8, column=0, padx=10, pady=20)

        # Create edit_frame widgets
        self.edit_data = {}
        self.edit_data['Name'] = EntryField(self.edit_frame, label='Name', error_message='', validate='key',
                                            validatecommand=self.validate_only_text)
        self.edit_data['Name'].grid(row=0, column=0, sticky=tk.W, padx=10, pady=2)
        self.edit_data['Name'].field.bind("<FocusOut>", self.validate_name)
        

        self.edit_data['Student_ID'] = EntryField(self.edit_frame, label='Student ID', error_message='', validate='key',
                                                  validatecommand=self.validate_only_numbers)
        self.edit_data['Student_ID'].grid(row=1, column=0, sticky=tk.W, padx=10, pady=2)
        self.edit_data['Student_ID'].field.bind("<FocusOut>", self.validate_ten_digits)
        

        self.edit_data['Date'] = CalendarField(self.edit_frame, label='Date')
        self.edit_data['Date'].grid(row=2, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.edit_data['Program'] = Combo(self.edit_frame, label='Program', options=('Anthropology', 'Art', 'Biology',
                                                                                 'Communication', 'Business'))
        self.edit_data['Program'].grid(row=3, column=0, sticky=tk.W, padx=10, pady=2)


        self.edit_data['Study_Year'] = RadiobuttonField(self.edit_frame, label='Year of Study',
                                                        options=['1', '2', '3', '4', '4+'], initial_value='1')
        self.edit_data['Study_Year'].grid(row=4, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.edit_data['Accessibility'] = RadiobuttonField(self.edit_frame, label='Registered with Accessibility?',
                                                           options=['Yes', 'No'], initial_value='No')
        self.edit_data['Accessibility'].grid(row=5, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.edit_data['Category'] = Combo(self.edit_frame, label='Category of Topic', options=('Registration',
                                                                                            'Finances', 'Transfer Credit',
                                                                                            'Personal Information',
                                                                                            'Petitions', 'Graduation',
                                                                                            'Exam Identification',
                                                                                            'Absence Declaration'))
        self.edit_data['Category'].grid(row=6, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.edit_data['Summary'] = ScrolledTextWidget(self.edit_frame, label='Summary of Question', error_message='')
        self.edit_data['Summary'].grid(row=7, column=0, sticky=tk.W, padx=10, pady=2)
        

        self.save_button = tk.Button(self.edit_frame, text='Save Changes', width=8, height=2, command=self.edit_selected)
        self.save_button.grid(row=8, column=0, padx=5, pady=20)

        self.cancel_button = tk.Button(self.edit_frame, text='Back', width=8, height=2, command=self.cancel_edit)
        self.cancel_button.grid(row=8, column=1, padx=5, pady=20)

        # Create directory_frame widgets
        self.directory_frame = tk.Frame(self.treeview_frame)
        self.directory_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
        
        # TREE ALPHA VERSION START
        scrollbarx = tk.Scrollbar(self.directory_frame, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(self.directory_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.directory_frame, columns=("ticket_id", "name", "date", 'program',
                                                                'study_year', 'category'),
                                 selectmode="browse", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
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
        self.tree.column('#4', stretch=tk.NO, minwidth=50, width=150)
        self.tree.column('#5', stretch=tk.NO, minwidth=50, width=90)
        self.tree.column('#6', stretch=tk.NO, minwidth=50, width=150)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.pack(fill='both', expand='true')
        self.selected = []

        # this object is the data persistence model
        self.persist = persist
        all_records = self.persist.get_all_sorted_records()
        # grab all records from db and add them to the treeview widget
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.date, record.program, record.study_year, record.category, record.summary))
        # TREE ALPHA VERSION END
            
        # Create treeview_frame widgets
        self.edit_button = tk.Button(self.treeview_frame, text='Edit', width=8, height=2, command=self.confirm_edit_record)
        self.edit_button.grid(row=1, column=0, pady=20)

        self.delete_button = tk.Button(self.treeview_frame, text='Delete', width=8, height=2, command=self.delete_selected)
        self.delete_button.grid(row=1, column=1, pady=20)

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

        # Initialize a flag to True. It will be set to False if any validation fails.
        can_submit = True

        # Reset error messages for each field before validation
        # I used ChatGPT for this code because it shortens the necessary (instead of manually checking if each field has a value)
        for field in self.edit_data.values():
            if hasattr(field, 'error'):
                field.error.configure(text='')

         # Validate each field and set the flag to False if validation fails
        if self.edit_data['Name'].get() == '':
            self.edit_data['Name'].error.configure(text='Please enter a name. This field is mandatory.')
            can_submit = False
        if self.edit_data['Student_ID'].get() == '':
            self.edit_data['Student_ID'].error.configure(text='Please enter a student ID. This field is mandatory.')
            can_submit = False
        if self.edit_data['Summary'].get() == '':
            self.edit_data['Summary'].error.configure(text='Please enter a summary of the question. This field is mandatory.')
            can_submit = False
        if self.edit_data['Program'].get() == '':
            self.edit_data['Program'].error.configure(text='Please enter a program. This field is mandatory.')
            can_submit = False
        if self.edit_data['Study_Year'].get() == '':
            self.edit_data['Study_Year'].error.configure(text='Please enter a year of study. This field is mandatory.')
            can_submit = False
        if self.edit_data['Accessibility'].get() == '':
            self.edit_data['Accessibility'].error.configure(text='Please confirm whether the student is registered with accessibility. This field is mandatory.')
            can_submit = False
        if self.edit_data['Category'].get() == '':
            self.edit_data['Category'].error.configure(text='Please enter the topic category. This field is mandatory.')
            can_submit = False

        # Only proceed with submission if all validations passed
        if can_submit:
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
        self.edit_frame.lift()
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
        
        # Initialize a flag to True. It will be set to False if any validation fails.
        can_submit = True

        # Reset error messages for each field before validation
        for field in self.data.values():
            if hasattr(field, 'error'):
                field.error.configure(text='')

        # Validate each field and set the flag to False if validation fails
        if self.data['Name'].get() == '':
            self.data['Name'].error.configure(text='Please enter a name. This field is mandatory.')
            can_submit = False
        if self.data['Student_ID'].get() == '':
            self.data['Student_ID'].error.configure(text='Please enter a student ID. This field is mandatory.')
            can_submit = False
        if self.data['Summary'].get() == '':
            self.data['Summary'].error.configure(text='Please enter a summary of the question. This field is mandatory.')
            can_submit = False
        if self.data['Program'].get() == '':
            self.data['Program'].error.configure(text='Please enter a program. This field is mandatory.')
            can_submit = False
        if self.data['Study_Year'].get() == '':
            self.data['Study_Year'].error.configure(text='Please enter a year of study. This field is mandatory.')
            can_submit = False
        if self.data['Accessibility'].get() == '':
            self.data['Accessibility'].error.configure(text='Please confirm whether the student is registered with accessibility. This field is mandatory.')
            can_submit = False
        if self.data['Category'].get() == '':
            self.data['Category'].error.configure(text='Please enter the topic category. This field is mandatory.')
            can_submit = False

        # Only proceed with submission if all validations passed
        if can_submit:
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
        if event.widget.get() and all(char.isalpha() or char.isspace() for char in event.widget.get()): # I used ChatGPT to learn about the event.widget.get() method
            self.data['Name'].error.configure(text='')
            self.edit_data['Name'].error.configure(text='')
        
        elif not event.widget.get():
            self.data['Name'].error.configure(text='Please enter a name. This field is mandatory.')
            self.edit_data['Name'].error.configure(text='Please enter a name. This field is mandatory.')
    
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

    def back_to_submit(self):
        self.data['Name'].error.configure(text='')
        self.edit_data['Name'].error.configure(text='')
        self.data['Student_ID'].error.configure(text='')
        self.edit_data['Student_ID'].error.configure(text='')
        self.data['Summary'].error.configure(text='')
        self.edit_data['Summary'].error.configure(text='')
        self.submit_frame.lift()

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
