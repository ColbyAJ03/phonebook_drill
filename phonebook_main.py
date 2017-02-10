#   Phone Book Drill
#
#   By Alexander Colby
#
#   For The Tech Academy
#
#   Python 3.5

from tkinter import *
import tkinter as tk

# import other modules
import phonebook_gui
import phonebook_func

# Frame is the Tkinter frame class that our own class will inherit from
class ParentWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # define master frame configuration
        self.master = master
        self.master.minsize(500,300)
        self.master.maxsize(500,300)
        # center app on user's screen
        phonebook_func.center_window(self,500,300)
        self.master.title('The Tkinter Phonebook Demo')
        self.master.configure(bg="white")
        # built in method to catch if the close button is clicked
        self.master.protocol('WM_DELETE_WINDOW', lambda: phonebook_func.ask_quit(self))
        arg = self.master

        # load in gui widgets from our other module
        phonebook_gui.load_gui(self)

# loop code        
if __name__ == '__main__':
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()
