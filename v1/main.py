import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from widgets import EntryField, Combo, RadiobuttonField, ScrolledTextWidget
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
        self.title("Demo1")

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

        # Left Frame
        left_frame_pad = 15
        self.left_frame = tk.Frame(self, relief="ridge", borderwidth=5)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame = tk.Frame(self, relief="ridge", borderwidth=5)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.name = EntryField(self.left_frame, label="Name")
        self.name.grid(row=0, column=0, sticky="nsew", pady=left_frame_pad)

        self.studentID = EntryField(self.left_frame, label="Studend ID")
        self.studentID.grid(row=1, column=0, sticky="nsew", pady=left_frame_pad)

        self.year = Combo(self.left_frame, label='Birth Year', options=('2003', '2004', '2005'))
        self.year.grid(row=3, column=0, sticky="nsew", pady=left_frame_pad)

        self.radiobutton_field = RadiobuttonField(self.left_frame, label="Year:", options=["Year 1", "Year 2", "Year 3", "Year 4+"])
        self.radiobutton_field.grid(row=4, column=0, sticky="nsew")

        self.button1 = Button(self.left_frame, text="Print Radio Button", width=20, command=lambda: {print(self.radiobutton_field.get())})
        self.button1.grid(row=5, column=0, sticky="nsew", pady=left_frame_pad)

        self.mature = RadiobuttonField(self.left_frame, label="Mature Student:",
                                                  options=["Yes", "No"])
        self.mature.grid(row=6, column=0, sticky="nsew", pady=left_frame_pad)

        self.accessibility = RadiobuttonField(self.left_frame, label="Registered with accessibility:",
                                       options=["Yes", "No"])
        self.accessibility.grid(row=7, column=0, sticky="nsew", pady=left_frame_pad)

        self.text_area = ScrolledTextWidget(self.left_frame, label="Enter Text:")
        self.text_area.grid(row=8, column=0)

        self.button1 = Button(self.left_frame, text="Print Scrolled Text", width=20,
                              command=lambda: {print(self.text_area.get())})
        self.button1.grid(row=9, column=0, sticky="nsew", pady=left_frame_pad)

        # Right Frame
        self.someother_label = tk.Label(self.right_frame, text="something")
        self.someother_label.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)  # This makes lower edge of frames touch the bottom of the screen


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