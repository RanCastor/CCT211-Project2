import tkinter as tk
import tkinter.ttk as ttk
import sys
from tkinter import scrolledtext
from tkcalendar import Calendar

class EntryField(tk.Frame):
    def __init__(self, parent, label='', error_message='', validate=None, validatecommand=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.dataentry = tk.StringVar()
        self.label = label
        self.error_message = error_message

        self.title = tk.Label(self, text=label, width=20)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))

        self.error = tk.Label(self,text=error_message, width=10)
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
    def __init__(self, parent, label='', options=('sasdf'), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.dataentry = tk.StringVar()
        self.label = label

        self.title = tk.Label(self, text=label, width=20)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))
        self.combo = ttk.Combobox(self, width=15, textvariable=self.dataentry, state="readonly")
        self.combo['values'] = options
        self.combo.grid(row=0, column=1, padx=15, pady=15, sticky=(tk.W + tk.E))
        self.combo.current()

    def reset(self):
        self.dataentry.set("")

    def get(self):
        return self.dataentry.get()


class RadiobuttonField(tk.Frame):
    def __init__(self, parent, label='', options=[], initial_value=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.choice = tk.StringVar(value=initial_value)

        self.label = tk.Label(self, text=label, width=20)
        self.label.grid(row=0, column=0, padx=10, pady=15, sticky=(tk.W + tk.E))

        self.option_buttons = []
        for index, option in enumerate(options):
            button = tk.Radiobutton(self, text=option, variable=self.choice, value=option)
            button.grid(row=0, column=index + 1, padx=5, sticky=(tk.W + tk.E))
            self.option_buttons.append(button)

    def reset(self):
        self.choice.set("")

    def get(self):
        return self.choice.get()


class ScrolledTextWidget(tk.Frame):
    def __init__(self, parent, label='', font=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = label

        if font is not None:
            self.custom_font = font
        else:
            self.custom_font = ("Arial", 10)  # Default font if not provided

        self.label = tk.Label(self, text=label, width=10)
        self.label.grid(row=0, column=0, padx=10, sticky=tk.W)

        self.scrolled_text = scrolledtext.ScrolledText(self, width=45, height=5, font=self.custom_font)
        self.scrolled_text.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    def reset(self):
        self.scrolled_text.delete("1.0", tk.END)

    def get(self):
        return self.scrolled_text.get("1.0", tk.END).strip()
    

# I consulted this sample code: https://www.geeksforgeeks.org/create-a-date-picker-calendar-tkinter/
class CalendarField(tk.Frame):
    def __init__(self, parent, selectmode='', year=None, month=None, day=None, label='', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = label
        self.title = tk.Label(self, text=label, width=20)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))

        self.cal = Calendar(self, selectmode = 'day', year = 2024, month = 3, day = 23)
        self.cal.grid(row=0, column=1, padx=15, pady = 20, sticky=(tk.W + tk.E))

        # tk.Button(self, text = "Get Date", command = self.grad_date).pack(pady = 20)
 
        # self.date = tk.Label(self, text = "")
        # self.date.pack(pady = 20)

    def grad_date(self):
        self.date.config(text = "Selected Date is: " + self.cal.get_date())
