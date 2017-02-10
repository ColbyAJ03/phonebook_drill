# script containing functions for phonebook_main

import os
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import sqlite3

# import other modules
import phonebook_main
import phonebook_gui

def center_window(self,w,h): # pass in the tkinter frame (master) reference and the width and height
    # get user's screen width and height
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()
    # calculate x and y coordinets to paint the app centered on the user's screen
    x = int((screen_width/2) - (w/2))
    y = int((screen_height/2) - (h/2))
    centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w,h,x,y))
    return centerGeo

# catch if user clicks to close window, prompts question to close
def ask_quit(self):
    if messagebox.askokcancel("Exit program", "Okay to exit application?"):
        # close the app
        self.master.destroy()
        os._exit(0)


#__________________________________________________________#

# create database
def create_db(self):
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE if not exists tbl_phonebook( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            col_fname TEXT, \
            col_lname TEXT, \
            col_fullname TEXT, \
            col_phone TEXT, \
            col_email TEXT \
            );")
        # commit() to save changes and close database connection
        conn.commit()
    conn.close()
    first_run(self)

def first_run(self):
    data = ('John','Doe','John Doe','111-111-1111','jdoe@email.com')
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur,count = count_records(cur)
        if count < 1:
            cur.execute("""INSERT INTO tbl_phonebook (col_fname,col_lname,col_fullname,col_phone,col_email) VALUES (?,?,?,?,?)""", (data))
            conn.commit()
    conn.close()

def count_records(cur):
    count = ""
    cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
    count = cur.fetchone()[0]
    return cur,count

# select item in Listbox
def onSelect(self,event):
    # calling the event is the self.lstList1 widget
    varList = event.widget
    select = varList.curselection()[0]
    value = varList.get(select)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT col_fname,col_lname,col_phone,col_email FROM tbl_phonebook WHERE col_fullname = (?)""", [value])
        varBody = cursor.fetchall()
        # return a tuple and slice it into 4 parts using data[] during the iteration
        for data in varBody:
            self.txt_fname.delete(0,END)
            self.txt_fname.insert(0,data[0])    
            self.txt_lname.delete(0,END)
            self.txt_lname.insert(0,data[1])
            self.txt_phone.delete(0,END)
            self.txt_phone.insert(0,data[2])
            self.txt_email.delete(0,END)
            self.txt_email.insert(0,data[3]) 

def addToList(self):
    var_fname = self.txt_fname.get()
    var_lname = self.txt_lname.get()
    # normalize the data to keep it consistent in the database
    var_fname = var_fname.strip() # removes any blank spaces before and after the user's entry
    var_lname = var_lname.strip()
    var_fname = var_fname.title() # capitalizes the first character of each word
    var_lname = var_lname.title()
    var_fullname = ("{} {}".format(var_fname,var_lname)) # combine normalized names into a full name
    print("var_fullname: {}".format(var_fullname))
    var_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()

    data = (var_fname,var_lname,var_fullname,var_phone,var_email)
    if (len(var_fname) > 0) and (len(var_lname) > 0) and (len(var_phone) > 0) and (len(var_email) > 0): # ensures fields are not left blank
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cursor = conn.cursor()
            # check db for duplicate full names
            cursor.execute("""SELECT COUNT(col_fullname) FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_fullname))
            count = cursor.fetchone()[0]
            chkName = count
            if chkName == 0: # if there are no duplicate full names, add new data
                print("chkName: {}".format(chkName))
                cursor.execute("""INSERT INTO tbl_phonebook(col_fname,col_lname,col_fullname,col_phone,col_email) VALUES(?,?,?,?,?)""", (data))
                self.lstList1.insert(END, var_fullname) # update listbox with new fullname
                onClear(self) # call the function to clear all of the textboxes
            else:
                messagebox.showerror("Name Error", "'{}' already exists in the database. Please choose a different name.".format(var_fullname))
                onClear(self) # call the function to clear all of the textboxes
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Missing Text Error","Please ensure that there is data in all of the fields.")


def onDelete(self):
    var_select = self.lstList1.get(self.lstList1.curselection()) # list box's selected value
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        # check to see if this is the last record or not
        # cannot delete the last record in the db
        cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cur.fetchone()[0]
        if count > 1:
            confirm = messagebox.askokcancel("Delete Confirmation", "All information associated with ({}) \nwill be permenantly deleted. \n\nProceed with the deletion request?".format(var_select))
            if confirm:
                conn = sqlite3.connect('phonebook.db')
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("""DELETE FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_select))
                onDeleted(self) # call function to clear all textboxes and selected index of listbox

                conn.commit()
        else:
            confirm = messagebox.showerror("Last Record Error", "({}) is the last record in the database and cannot be deleted. \n\nPlease add another record before you delete ({}).".format(var_select, var_select))
    conn.close()


def onDeleted(self):
    # delete info in the textboxes
    self.txt_fname.delete(0,END)
    self.txt_lname.delete(0,END)
    self.txt_phone.delete(0,END)
    self.txt_email.delete(0,END)
    try:
        index = self.lstList1.curselection()[0]
        self.lstList1.delete(index)
    except IndexError:
        pass


def onClear(self):
    # clear text in all textboxes
    self.txt_fname.delete(0,END)
    self.txt_lname.delete(0,END)
    self.txt_phone.delete(0,END)
    self.txt_email.delete(0,END)

    
def onRefresh(self):
    # populate listbox coinciding with the database
    self.lstList1.delete(0,END)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cursor.fetchone()[0]
        i = 0
        while i < count:
            cursor.execute("""SELECT col_fullname FROM tbl_phonebook""")
            varList = cursor.fetchall()[i]
            for item in varList:
                self.lstList1.insert(0,str(item))
                i += 1
    conn.close()

def onUpdate(self):
    try:
        var_select = self.lstList1.curselection()[0] # index of list selection
        var_value = self.lstList1.get(var_select)    # list selection's text value
    except:
        messagebox.showinfo("Missing selection", "No name was selected from the list. \nCancelling the Update request.")
        return
    # the user will only be allowed to update changes to the phone and email
    # for name changes, the user will need to delete the entire record and add it again
    var_phone = self.txt_phone.get().strip() # normalize data to maintain db integrity
    var_email = self.txt_email.get().strip()
    if (len(var_phone) > 0) and len(var_email) > 0: # make sure data is present
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            # count records to see if changes are already in the database (update or not)
            cur.execute("""SELECT COUNT(col_phone) FROM tbl_phonebook WHERE col_phone = '{}'""".format(var_phone))
            count = cur.fetchone()[0]
            print (count)
            cur.execute("""SELECT COUNT(col_email) FROM tbl_phonebook WHERE col_email = '{}'""".format(var_email))
            count2 = cur.fetchone()[0]
            print (count2)
            if count == 0 or count2 == 0: # if changes are not already present, then proceed
                response = messagebox.askokcancel("Update Request", "The following changes ({}) and ({}) will be implemented for ({}).".format(var_phone, var_email, var_value))
                print (response)
                if response:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("""UPDATE tbl_phonebook SET col_phone = '{0}', col_email = '{1}' WHERE col_fullname = '{2}'""".format(var_phone, var_email, var_value))
                        onClear(self)
                        conn.commit()
                else:
                    messagebox.showinfo("Cancel request", "No changes have been made to ({}).".format(var_value))
            else:
                messagebox.showinfo("No changes detected", "Both ({}) and ({}) \nalready exist in the database for this name.".format(var_phone, var_email))
            onClear(self)
        conn.close()
    else:
        messagebox.showerror("Missing Info", "Please select a name from the list \nthen edit the phone or email info.")
    onClear(self)

if __name__ == "__main__":
    pass
        
            
                


    
