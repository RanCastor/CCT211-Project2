import tkinter as tk
import tkinter.ttk as ttk
import sys
from tkinter import scrolledtext
from tkcalendar import Calendar
from datetime import datetime

class EntryField(tk.Frame):
    def __init__(self, parent, label='', error_message='', validate=None, validatecommand=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.dataentry = tk.StringVar()
        self.label = label
        self.error_message = error_message

        self.title = tk.Label(self, text=label, width=20)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))

        self.error = tk.Label(self, text=error_message, width=10, fg='red')
        self.error.grid(row=1, column=0, columnspan=2, sticky=(tk.W + tk.E))
        
        # Register the validation command with the widget's interpreter
        if validatecommand:
            wrapped_function = self.register(validatecommand)
            vcmd = (wrapped_function,'%P')
        else:
            vcmd = None

        # I used ChatGPT to find a way to pass arguments that were passed to the parent (frame) to the child (entry)
        # This way, the arguments passed to the parent are first stored in a dictionary then passed to the child
        # The entry is not created at the same time as the frame
        entry_options = {
            'width': 30,
            'textvariable': self.dataentry,
            'validate': validate,
            'validatecommand': vcmd,
        }

        self.field = tk.Entry(self, **entry_options) # This line unpacks the entry_options dictionary and passes the arguments to the entry
        self.field.grid(row=0, column=1, padx=15, sticky=(tk.W + tk.E))

    def reset(self):
        self.dataentry.set("")

    def get(self):
        return self.dataentry.get()


class Combo(tk.Frame):
    def __init__(self, parent, label='', error_message='', options=('sasdf'), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.dataentry = tk.StringVar()
        self.label = label
        self.error_message = error_message

        self.title = tk.Label(self, text=label, width=20)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))
        self.combo = ttk.Combobox(self, width=15, textvariable=self.dataentry, state="readonly")
        self.combo.bind("<<ComboboxSelected>>", self.validate_selection)
        self.combo['values'] = options
        self.combo.grid(row=0, column=1, padx=15, pady=15, sticky=(tk.W + tk.E))
        self.combo.current()

        self.error = tk.Label(self, text=error_message, width=10, fg='red')
        self.error.grid(row=1, column=0, columnspan=2, sticky=(tk.W + tk.E))

    def reset(self):
        self.dataentry.set("")

    def get(self):
        return self.dataentry.get()
    
    def validate_selection(self, event):
        if self.dataentry.get():
            self.error.config(text='')
        else:
            self.error.config(text=self.error_message)


class RadiobuttonField(tk.Frame):
    def __init__(self, parent, label='', error_message='', options=[], initial_value=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.choice = tk.StringVar(value=initial_value)
        self.error_message = error_message

        self.label = tk.Label(self, text=label, width=20)
        self.label.grid(row=0, column=0, padx=10, pady=15, sticky=(tk.W + tk.E))

        self.error = tk.Label(self, text=error_message, fg='red')
        self.error.grid(row=5, column=1, columnspan=5, sticky=(tk.W + tk.E))

        self.option_buttons = []
        for index, option in enumerate(options):
            button = tk.Radiobutton(self, text=option, variable=self.choice, value=option)
            button.bind("<ButtonRelease-1>", self.validate_selection)
            button.grid(row=0, column=index + 1, padx=5, sticky=(tk.W + tk.E))
            self.option_buttons.append(button)

    def reset(self):
        self.choice.set("")

    def get(self):
        return self.choice.get()
    
    def validate_selection(self, event):
        if self.choice.get():
            self.error.config(text='')
        else:
            self.error.config(text=self.error_message)


class View_ScrolledTextWidget(tk.Frame):
    def __init__(self, parent, font=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        if font is not None:
            self.custom_font = font
        else:
            self.custom_font = ("Arial", 10)  # Default font if not provided

        self.scrolled_text = scrolledtext.ScrolledText(self, width=45, height=7, font=self.custom_font)
        self.scrolled_text.grid(row=0, column=1, sticky=tk.W)

        self.scrolled_text.config(state=tk.DISABLED)

    def reset(self):
        self.scrolled_text.delete("1.0", tk.END)

    def get(self):
        return self.scrolled_text.get("1.0", tk.END).strip()


class ScrolledTextWidget(tk.Frame):
    def __init__(self, parent, label='', error_message='', font=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = label
        self.error_message = error_message

        if font is not None:
            self.custom_font = font
        else:
            self.custom_font = ("Arial", 10)  # Default font if not provided

        self.label = tk.Label(self, text=label, width=20)
        self.label.grid(row=0, column=0, padx=10, sticky=tk.W)

        self.error = tk.Label(self, text=error_message, width=10, fg='red')
        self.error.grid(row=1, column=0, columnspan=2, sticky=(tk.W + tk.E))

        self.scrolled_text = scrolledtext.ScrolledText(self, width=45, height=5, font=self.custom_font)
        self.scrolled_text.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.scrolled_text.bind("<Key>", self.validate_question)
        # self.scrolled_text.bind("<Key>", self.limit_chars)
        self.scrolled_text.bind("<FocusOut>", self.validate_fifty_chars)

    def reset(self):
        self.scrolled_text.delete("1.0", tk.END)

    def get(self):
        return self.scrolled_text.get("1.0", tk.END).strip()
    
    '''
    # I used ChatGPT to obtain the limit_chars method because it's not possible to use validatecommand for scrolledtext widgets like for entries,
    # so I didn't know how to restrain the user from inputing over 50 chars
    def limit_chars(self, event):
        # Allow backspace and delete keys to always work
        if event.keysym in ("BackSpace", "Delete"):
            # You still want to clear the error message if the content length is now below 50
            self.update_error_message()
            return

        # Get the current content and check the length
        current_content = self.get()  # Using your get method that strips the trailing newline
        content_length = len(current_content)

        if content_length >= 50 and event.char:
            # Set the error message if over the limit and the key pressed would add a character
            self.error.configure(text='Please limit the summary to 50 characters')
            return "break"  # Prevent further characters from being added
        else:
            # Update or clear the error message based on the current content length
            self.update_error_message()

    '''

    def update_error_message(self):
        """Updates the error message based on the current text length."""
        current_content = self.get()
        if len(current_content) > 50:
            self.error.configure(text='Please limit the summary to 50 characters')
        else:
            self.error.configure(text='')  # Clear the error message
    
    def validate_fifty_chars(self, event):
        text = self.get()
        if text and len(text) > 50:
            self.error.configure(text='Please limit the summary to 50 characters')
        elif text == '':
            self.error.configure(text='Please enter a summary of the question. This field is mandatory.')
        else:
            self.error.configure(text='')

    # I used ChatGPT to obtain the code for most of the validate_question method because it's not possible to use validatecommand for scrolledtext widgets like for entries,
    # so I didn't know how to restrain the user from inputing over 50 chars
    def validate_question(self, event):
        # Allow certain control keys without validation
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
            return

        # Predict the content after the key press
        current_content = self.get()
        predicted_content = current_content + event.char
    
        # Validate the predicted content
        question_valid = len(predicted_content) <= 50 and all(
            char.isalpha() or char.isspace() or char.isdigit() or char in ',.' for char in predicted_content)
    
        if not question_valid:
            # Prevent the character from being added
            self.error.configure(text='Please do not enter special characters and limit the summary to 50 characters')
            return "break"
        else:
            # Clear the error message if the input is valid
            self.update_error_message()

# I consulted this sample code: https://www.geeksforgeeks.org/create-a-date-picker-calendar-tkinter/
class CalendarField(tk.Frame):
    def __init__(self, parent, selectmode='', year=None, month=None, day=None, label='', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = label
        self.title = tk.Label(self, text=label, width=20)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))

        self.cal = Calendar(self, selectmode = 'day', year = datetime.now().date().year, month = datetime.now().date().month, day = datetime.now().date().day)
        self.cal.grid(row=0, column=1, padx=15, pady = 20, sticky=(tk.W + tk.E))

        # tk.Button(self, text = "Get Date", command = self.grad_date).pack(pady = 20)
 
        # self.date = tk.Label(self, text = "")
        # self.date.pack(pady = 20)

    def grad_date(self):
        self.date.config(text = "Selected Date is: " + self.cal.get_date())

    def reset(self):
        self.cal.year, self.cal.month, self.cal.day = datetime.now().date().year, datetime.now().date().month, datetime.now().date().day

    def get(self):
        return self.cal.get_date()
