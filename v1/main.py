import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from tkinter import messagebox
from widgets import EntryField, Combo, RadiobuttonField, ScrolledTextWidget, CalendarField
import tkinter.ttk as ttk  # just for treeview
# import entry_field  # no particular good reason I did it the other way here
# from models import *  # done this way to access classes just by name
import sys  # only used for flushing debug print statements


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # this is the main database access object
        # note you must run the init_db.py script before using SQLStorage
        # self.data = SQLStorage()

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
            frame = F(parent=container, controller=self)
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
        self.name_field = EntryField(self.frame1, label='Name', error_message='', validate='key', validatecommand=self.validate_only_text)
        self.name_field.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_field.field.bind("<FocusOut>", self.validate_name)

        self.id_field = EntryField(self.frame1, label='Student ID', error_message='', validate='key', validatecommand=self.validate_only_numbers)
        self.id_field.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_field.field.bind("<FocusOut>", self.validate_ten_digits)

        self.cal = CalendarField(self.frame1, label='Date')
        self.cal.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.program = Combo(self.frame1, label='Program', options=('Anthropology', 'Art', 'Biology', 'Communication', 'Business'))
        self.program.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self.year_of_study = RadiobuttonField(self.frame1, label='Year of Study', options=['1', '2', '3', '4', '4+'], initial_value='1')
        self.year_of_study.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.accessibility = RadiobuttonField(self.frame1, label='Registered with Accessibility?', options=['Yes', 'No'], initial_value='No')
        self.accessibility.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)

        self.topic = Combo(self.frame1, label='Category of Topic', options=('Registration', 'Finances', 'Transfer Credit', 'Personal Information', 'Petitions', 'Graduation', 'Exam Identification', 'Absence Declaration'))
        self.topic.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)

        self.question = ScrolledTextWidget(self.frame1, label='Summary of Question', error_message='')
        self.question.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

        self.submit_button = tk.Button(self.frame1, text='Submit', width=4, height=2)
        self.submit_button.grid(row=8, column=0, padx=10, pady=30)

        # Create frame3 widgets
        self.edit_name_field = EntryField(self.frame3, label='Name', error_message='', validate='key', validatecommand=self.validate_only_text)
        self.edit_name_field.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.edit_name_field.field.bind("<FocusOut>", self.validate_name)

        self.edit_id_field = EntryField(self.frame3, label='Student ID', error_message='', validate='key', validatecommand=self.validate_only_numbers)
        self.edit_id_field.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.edit_id_field.field.bind("<FocusOut>", self.validate_ten_digits)

        self.edit_cal = CalendarField(self.frame3, label='Date')
        self.edit_cal.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_program = Combo(self.frame3, label='Program', options=('Anthropology', 'Art', 'Biology', 'Communication', 'Business'))
        self.edit_program.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_year_of_study = RadiobuttonField(self.frame3, label='Year of Study', options=['1', '2', '3', '4', '4+'], initial_value='1')
        self.edit_year_of_study.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_accessibility = RadiobuttonField(self.frame3, label='Registered with Accessibility?', options=['Yes', 'No'], initial_value='No')
        self.edit_accessibility.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_topic = Combo(self.frame3, label='Category of Topic', options=('Registration', 'Finances', 'Transfer Credit', 'Personal Information', 'Petitions', 'Graduation', 'Exam Identification', 'Absence Declaration'))
        self.edit_topic.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)

        self.edit_question = ScrolledTextWidget(self.frame3, label='Summary of Question', error_message='')
        self.edit_question.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

        self.submit_button = tk.Button(self.frame3, text='Save Changes', width=8, height=2)
        self.submit_button.grid(row=8, column=0, padx=5, pady=30)

        self.cancel_button = tk.Button(self.frame3, text='Cancel', width=4, height=2, command=self.cancel_edit)
        self.cancel_button.grid(row=8, column=1, padx=5, pady=30)


        # Create frame2 widgets
        # self.see_directory_button = tk.Button(self.frame2, text='See Directory', command=self.go_to_directory)
        # self.see_directory_button.grid(row=0, column=0, padx=10, pady=10)

        # self.see_submission_button = tk.Button(self.frame2, text='See Submission', command=self.go_to_profile)
        # self.see_submission_button.grid(row=0, column=1, padx=10, pady=10)

        self.directory_frame = tk.Frame(self.frame2, bg='yellow', width=850, height=600)
        self.directory_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        # self.profile_frame = tk.Frame(self.frame2, bg='green', width=850, height=600)
        # self.profile_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        self.edit_button = tk.Button(self.frame2, text='Edit', width=8, height=2, command=self.confirm_edit_record)
        self.edit_button.grid(row=2, column=0, pady=20)

        self.delete_button = tk.Button(self.frame2, text='Delete', width=8, height=2, command=self.confirm_delete_record)
        self.delete_button.grid(row=2, column=1, pady=20)
        
        self.grid_rowconfigure(0, weight=1)  # This makes lower edge of frames touch the bottom of the screen
         
    
    def validate_only_text(self, text):
        # Check if input text is valid
        name_valid = len(text) <= 1000 and all(char.isalpha() or char.isspace() for char in text) # I used ChatGPT to learn about the all() function
        
        if name_valid:
            # Clear error message
            self.name_field.error.configure(text='')
            self.edit_name_field.error.configure(text='')
        else:
            # Display error message
            self.name_field.error.configure(text='Please only enter letters or spaces')
            self.edit_name_field.error.configure(text='Please only enter letters or spaces')
        
        return name_valid

    # This verifies if the name is correct when the user clicks away from the entry and clears error messages accordingly
    def validate_name(self, event):
        if all(char.isalpha() or char.isspace() for char in event.widget.get()): # I used ChatGPT to learn about the event.widget.get() method
            self.name_field.error.configure(text='')
            self.edit_name_field.error.configure(text='')
        else:
            self.name_field.error.configure(text='Please only enter letters or spaces')
            self.edit_name_field.error.configure(text='Please only enter letters or spaces')

    def validate_only_numbers(self, text):
        # Check if input text is valid
        id_valid = len(text)<=10 and all(char.isdigit() for char in text)

        if id_valid:
            # Clear error message
            self.id_field.error.configure(text='')
            self.edit_id_field.error.configure(text='')
        else:
            # Display error message
            self.id_field.error.configure(text='Please enter the ten digits only composed of numbers')
            self.edit_id_field.error.configure(text='Please enter the ten digits only composed of numbers')
        
        return id_valid

    def validate_ten_digits(self, event):
        if len(event.widget.get()) != 10:
            self.id_field.error.configure(text='The Student ID must be 10 digits long')
            self.edit_id_field.error.configure(text='The Student ID must be 10 digits long')
        elif len(event.widget.get()) == 10:
            self.id_field.error.configure(text='')
            self.edit_id_field.error.configure(text='')

    # def go_to_directory(self):
        # self.directory_frame.lift()

    # def go_to_profile(self):
        # self.profile_frame.lift()

    def go_to_edit(self):
        #TO DO: populate widgets with data in the selected record
        self.name_field.error.configure(text='')
        self.edit_name_field.error.configure(text='')
        self.id_field.error.configure(text='')
        self.edit_id_field.error.configure(text='')
        self.question.error.configure(text='')
        self.edit_question.error.configure(text='')
        self.name_field.reset()
        self.id_field.reset()
        self.question.reset()
        self.frame3.lift()

    def back_to_submit(self):
        self.name_field.error.configure(text='')
        self.edit_name_field.error.configure(text='')
        self.id_field.error.configure(text='')
        self.edit_id_field.error.configure(text='')
        self.question.error.configure(text='')
        self.edit_question.error.configure(text='')
        self.frame1.lift()
        

    def confirm_delete_record(self):
        confirm_delete = messagebox.askokcancel("Delete", "Are you sure you want to delete this record?")
        if confirm_delete:
            #TO DO: add code to delete record
            pass

    def confirm_edit_record(self):
        confirm_edit = messagebox.askokcancel("Edit", "Are you sure you want to edit this record? Any data yet to be submitted or saved will be lost.")
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
