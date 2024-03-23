import tkinter as tk
import tkinter.ttk as ttk
import sys
from tkinter import scrolledtext


class EntryField(tk.Frame):
    def __init__(self, parent, label='', passwordField=False, *args, **kwargs):
        # keep in mind EntryField is a Frame widget so any args and kwargs apply only to it, not its children - the label and title
        super().__init__(parent, *args, **kwargs)
        self.dataentry = tk.StringVar()
        self.label = label

        self.title = tk.Label(self, text=label, width=10)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))
        # args and kwargs are only sent in the super and this doesn't apply to the super construct but one of the children
        if passwordField:
            self.field = tk.Entry(
                self, width=30, textvariable=self.dataentry, show="*")
        else:
            self.field = tk.Entry(
                self, width=30, textvariable=self.dataentry)
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

        self.title = tk.Label(self, text=label, width=10)
        self.title.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))
        self.combo = ttk.Combobox(self, width=15, textvariable=self.dataentry, state="readonly")
        self.combo['values'] = options
        self.combo.grid(row=0, column=1, padx=15, sticky=(tk.W + tk.E))
        self.combo.current()

    def reset(self):
        self.dataentry.set("")

    def get(self):
        return self.dataentry.get()


class RadiobuttonField(tk.Frame):
    def __init__(self, parent, label='', options=[], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.dataentry = tk.StringVar()

        self.label = tk.Label(self, text=label, width=25)
        self.label.grid(row=0, column=0, padx=10, sticky=(tk.W + tk.E))

        self.option_buttons = []
        for index, option in enumerate(options):
            button = tk.Radiobutton(self, text=option, variable=self.dataentry, value=option)
            button.grid(row=0, column=index + 1, padx=5, sticky=(tk.W + tk.E))
            self.option_buttons.append(button)

    def reset(self):
        self.dataentry.set("")

    def get(self):
        return self.dataentry.get()


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

        self.dataentry = scrolledtext.ScrolledText(self, width=45, height=5, font=self.custom_font)
        self.dataentry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    def reset(self):
        self.dataentry.delete("1.0", tk.END)

    def get(self):
        return self.dataentry.get("1.0", tk.END).strip()