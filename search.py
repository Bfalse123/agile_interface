#libs for GUI
import tkinter as tk #Event-driven graphics library (GUI)
from tkinter import messagebox #Context windows
from tkinterdnd2 import DND_FILES #Extension of tkinter for drag and drop mechanism support

import os #Library for searching dirs and files 
import re #Library for regexes

import pandas as pd #Pandas to read csv files

DATA_DIR = "data_tables/" #Constant: dir for csv files

def parse_data_files():
	"""
Function to include all the csv files in the directory DATA_DIR
	Uses:
		os
		os.path
		tkinter -> messagebox
	Returns dictionary:
		keys - file names
		values - file path
	"""
	path_dict = dict()
	if os.path.exists(DATA_DIR):
		files = os.listdir(DATA_DIR)
		for file in files:
			if file.endswith(".csv"):
				path_dict[file] = os.path.abspath(DATA_DIR + file)
		if len(path_dict.keys()) == 0:
			print(f"\033[33m.csv files in {DATA_DIR} were not found\033[0m")
			messagebox.showinfo(".csv files were not found", "Data dir is empty, you can put .csv files there")
			return path_dict
	else:
		print(f"\033[33mData dir ({DATA_DIR}) is missing -> Creating\033[0m")
		os.mkdir(DATA_DIR)
		messagebox.showinfo("Data dir does not exists", "Data dir was created, you can put .scv files there")
		return path_dict
	print(f"\033[32mFiles from {DATA_DIR} were added:\033[0m", *path_dict)
	print(path_dict)
	return path_dict

class Search():
	"""
Class of application main frame widgets:
Contains widgets:
	main_frame(frame) - root frame
		files(frame)
			files_listbox(listbox)
			title_files_listbox(label)
		search(frame)
			search_entrybox(entry)
			title_search_entrybox(label)
Contains events:
	DROP -> drop_inside_files_listbox -> inserts .scv into application
	DOUBLE MOUSE click -> display_file -> changes current shown file
	ENTER key -> search_table -> apply search request
	"""
	def __init__(self, parent, data):
		self.path_dict = parse_data_files() #Returns dict with all csv files into DATA_DIR
		self.files = tk.Frame(parent, background="#33084f") #Frame for all uploaded files
		self.files_listbox = tk.Listbox(self.files, selectmode=tk.SINGLE, #Creates listbox for list of csv files
										background="#c5a7d9", selectbackground="#2e0847", 
										foreground="#262626", font="Cambria 12",
										highlightcolor="#2e0847", relief=tk.FLAT,
										bd=4, highlightthickness=2,
										height = 10, width=20,
										listvariable=tk.Variable(value=list(self.path_dict)))
		self.title_files_listbox = tk.Label(self.files, text="UPLOADED FILES", #Creates titile for listbox files_listbox
											background="#33084f", justify=tk.CENTER, 
											foreground="#ffffff", font="Cambria 14 bold")
		self.title_files_listbox.pack() #Adding the title on the frame files
		self.files_listbox.pack(fill=tk.BOTH, expand=True, padx=11, pady=9) #Adding the listbox on the frame files
		self.files.pack(ipadx=10, fill=tk.Y, side=tk.LEFT) #Adding the files frame to application main frame
		
		self.files_listbox.drop_target_register(DND_FILES) #Adds opportunity to drag and drop files into listbox
		self.files_listbox.dnd_bind("<<Drop>>", self.drop_inside_files_listbox) #Linking event and method: dropping files cause call of drop_inside_files_listbox method
		self.files_listbox.bind("<Double-Button-1>", self.display_file) #Linking event and method: double mouse click on the file cause switch on other file

		self.search = tk.Frame(parent, background="#05282b") #Frame for search field
		self.entrybox_text = tk.StringVar() #connection with text of input field
		self.search_entrybox = tk.Entry(self.search, textvariable=self.entrybox_text, #Creates field for user's input
										background="#0a646e", font="Cambria 14")
		self.title_search_entrybox = tk.Label(self.search, text="SEARCH:", #Creates title for user's input field
											background="#05282b", justify=tk.CENTER, 
											foreground="#ffffff", font="Cambria 14 bold")

		self.title_search_entrybox.pack(side=tk.LEFT, anchor=tk.W) #Adding the title into search frame
		self.search_entrybox.pack(fill=tk.BOTH, expand=True, padx=5, pady=8) #Addint input field into search frame
		self.search.pack(ipady=10, fill=tk.X, side=tk.TOP) #Adding the search frame to application main frame
		self.search_entrybox.bind("<KeyPress-Return>", self.search_table) #Linking event and method: pressing enter key cause call of search_table method 
		self.data_table = data #implementation of Data class object
		self.data_table.place(
            rely=0.08,
            relx=0.17,
            relwidth=0.9,
            relheight=0.95)
		

	def drop_inside_files_listbox(self, event): #adding dropped files into system
		log = list()
		file_paths = re.findall(r"(?<=\{).+?(?=\})", event.data)
		for file_path in file_paths:
			if file_path.endswith(".csv"):
				file_name = os.path.basename(file_path)
				if file_name not in self.path_dict.keys():
					self.files_listbox.insert(tk.END, file_name)
					self.path_dict[file_name] = file_path
					log.append(file_name)
		if len(log) != 0:
			print(f"\033[32mFiles from DROP were added:\033[0m", *log)
			messagebox.showinfo("Files adding", "Files {} were successfuly added".format(", ".join(log)))	
		else:
			print(f"\033[31mDROP was unsuccessful -> files:\033[0m", *file_paths)
			messagebox.showerror("DROP error", "Add at least one .csv file with unique name")

	def display_file(self, event): #method to change current file to show
		file_name = self.files_listbox.get(self.files_listbox.curselection())
		path = self.path_dict[file_name]
		print(f"\033[32mFile {path} has been chosen -> reading\033[0m")
		df = pd.read_csv(path, encoding='utf-8') #Uses only comma separator
		print(df)
		self.data_table.set_datatable(dataframe=df)

	def search_table(self, event): #method to search into table
		entry = self.entrybox_text.get()
		print(entry)
		self.data_table.find_value(entry)
