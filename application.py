#Libraries for GUI
import tkinter as tk #Event-driven graphics library (GUI)
from tkinter import messagebox #Context windows
from tkinterdnd2 import TkinterDnD #Extension of tkinter for drag and drop mechanism support

class Application(TkinterDnD.Tk):
	"""
Class of application entity:
Inherited by TkinterDND class -> uses Tkinter library with adding drag-and-drop mechanism
Creates the window that is able to response on users inputs
Includes:
	finish method -> determine behaviour of programm in explicit terminating of the program by window manager
	constuctor -> creates window and frame in it. The frame will be used by another class to put table info into it
	"""
	def finish(self):
		if messagebox.askokcancel("Quite", "Do you want to quite?"):
			self.destroy()
			print("\033[32mThe application has been successfully terminated\033[0m")
		else:
			print("\033[31mExiting the application has been canceled\033[0m")
	
	def __init__(self):
		super().__init__() #Performs default constructor of TkinterDND.Tk class creating object of toplevel Tk widget(window)
		self.title("Purchases")
		self.geometry("1366x768+10+10")
		self.iconbitmap(default="include/root_icon.ico")
		self.minsize(700, 400)
		self.update_idletasks()
		
		self.protocol("WM_DELETE_WINDOW", self.finish) #Handler for cases when the user explicitly closes a window using the window manager
		
		self.main_frame = tk.Frame(self, background="#e8eeff") #Widgets container(frame)
		self.main_frame.pack(fill=tk.BOTH, expand=True) #Place frame into window
		print("\033[32mThe application has been successfully launched\033[0m")