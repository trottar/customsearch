#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2020-03-09 12:10:02 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

import functools
import tkinter as tk
from tkinter import filedialog

fields = 'To', 'cc', 'Subject'

body = 'Body'

email_entries = []

# Check if a function was called, see function below @calltracker
def calltracker(func):
    @functools.wraps(func)
    def wrapper(*args):
        wrapper.has_been_called = True
        return func(*args)
    wrapper.has_been_called = False
    return wrapper

# Perfrom multiple functions 
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def fetch(entries):
    for entry in entries:
        if isinstance(entry[1],tk.Entry):
            field = entry[0]
            text  = entry[1].get()
            print('%s: "%s"' % (field, text))
            email_entries.insert(0,text)
        elif isinstance(entry[1],tk.Text):
            field = entry[0]
            text  = entry[1].get("1.0",tk.END)
            print('%s: "%s"' % (field, text))
            email_entries.insert(0,text)
        else:
            print("Invalid entry")
            exit
    return email_entries
            
def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    TextArea = tk.Text(root)
    ScrollBar = tk.Scrollbar(root)
    ScrollBar.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=ScrollBar.set)
    ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    TextArea.pack(expand=tk.YES, fill=tk.BOTH)
    entries.append((body,TextArea))
    return entries

@calltracker
def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    email_entries.append(filename)

def createGUI():
    root = tk.Tk()
    ents = makeform(root, fields)
    b1 = tk.Button(root, text='Send',command=combine_funcs((lambda e=ents: fetch(e)),root.quit))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Discard', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Attachment', command=UploadAction)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
    return email_entries

def main():
    createGUI()
    
if __name__ == '__main__': main()
