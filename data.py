#Libraries for smart search
#!Should add annotation to each one
import nltk  #Natural Language Toolkit - library for Natural Language Processing
from nltk.corpus import stopwords  #Package of nltk to read corpus files
from pymorphy2 import MorphAnalyzer #Morphological analyzer for the Russian language
from sklearn.feature_extraction.text import TfidfVectorizer  #Machine learning library
from sklearn.metrics.pairwise import cosine_distances #Module for clustering metrics
from razdel import tokenize #Library to tokenize russian sentences
import pandas as pd #Library added to read csv files

#Libraries for GUI
import tkinter as tk #Event-driven graphics library (GUI)
from tkinter import messagebox #Context windows
from tkinter import ttk #Exension for tkinter themed widgets

import numpy as np #Library to work with arrays and matrixes

DESCRIBING_COLUMN = "tokenz" #Constant: label of column in .scv file, which describes data
QUERY_RESULT_LEN = 30 #Constant: number of showing elements for search query response

class Data():
	"""
	Representation of data class
	"""
	def __init__(self, parent):
		self.data = tk.Frame(parent, background="#deb5ff")
		
		self.table = ttk.Treeview(self.data)

		self.file_name = tk.Label(self.data, text="",
								background="#a5fae5", justify=tk.CENTER, 
								foreground="#1f302c", font="Cambria 12")

		# create scroll objects
		self.scroll_Y = tk.Scrollbar(self.data, orient=tk.VERTICAL, command=self.table.yview)
		self.scroll_X = tk.Scrollbar(self.data, orient=tk.HORIZONTAL, command=self.table.xview)
		
		self.table.configure(yscrollcommand=self.scroll_Y.set, xscrollcommand=self.scroll_X.set)
		
		self.file_name.pack(side=tk.TOP, fill=tk.X)
		self.scroll_Y.pack(side=tk.RIGHT, fill=tk.Y)
		self.scroll_X.pack(side=tk.BOTTOM, fill=tk.X)
		self.table.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)
		self.data.place(rely=0.08, relx=0.17, relwidth=0.83, relheight=0.918)

		# Object of class MorphAnalyzer to determine russian words characteristics
		self.morph = MorphAnalyzer()

		# Object of class TfidfVectorizer to convert text to word frequency vectors
		self.tfidf = TfidfVectorizer()

		# Downloading stopwords list (words with little meaning)
		nltk.download('stopwords')
		self.stopwords_ru = stopwords.words('russian')

		self.stored_dataframe = None
		self.tfidf_features = None

	def set_dataframe(self, path):
		print(f"\033[33mReading chosen .csv file...\033[0m")
		dataframe = pd.read_csv(path, encoding='utf-8') #Uses only comma separator
		print(f"\033[32mChosen .csv file was successfully read\033[0m")
		if DESCRIBING_COLUMN not in dataframe.columns:
			messagebox.showerror("FILE_FORMAT error", f"Chosen file does not have \"{DESCRIBING_COLUMN}\" column")
			print(f"\033[31mFile {path} does not have column for search through: {DESCRIBING_COLUMN}\033[0m")
			return
		self.file_name.config(text=path)
		self.stored_dataframe = dataframe
		self.tfidf_features = self.tfidf.fit_transform(self.stored_dataframe[DESCRIBING_COLUMN])
		self.draw_table(self.stored_dataframe)
	
	def draw_table(self, dataframe):
		self.table.delete(*self.table.get_children(""))
		columns = list(dataframe.columns)
		
		self.table.__setitem__("show", "headings")
		self.table.__setitem__("column", columns)
		for col in columns:
			self.table.heading(col, text=col)

		dataframe_rows = dataframe.to_numpy().tolist()
		for row in dataframe_rows:
			self.table.insert("", "end", values=row)

	def tokens(self, entry):
		token_list = list(tokenize(entry))
		result_list = list()
		for token in token_list:
			if token.text not in self.stopwords_ru:
				string = self.morph.normal_forms(token.text)[0]
				if string not in ")(][:\\/|":
					result_list.append(string)
		return result_list

	def tff(self, query):
		q_tokens = self.tokens(query)
		q_tokens_transform = self.tfidf.transform(q_tokens)
		cosine_dist = cosine_distances(self.tfidf_features, q_tokens_transform)[:, 0]
		half_len_dataframe = len(self.stored_dataframe) // 2
		qrl = QUERY_RESULT_LEN if QUERY_RESULT_LEN < half_len_dataframe else half_len_dataframe
		indices = np.argsort(cosine_dist)[0 : qrl]
		return indices

	def find_value(self, query):
		qri = self.tff(query)
		indices = ["res_" + str(index) for index in range(len(qri))]
		df_qr = pd.DataFrame(
							columns=self.stored_dataframe.columns,
							index = indices
							)
		for index in range(len(qri)):
			df_qr.loc[indices[index]] = self.stored_dataframe.iloc[qri[index]]
		self.draw_table(df_qr)

	def reset_table(self):
		print(f"\033[33mReseting the table...\033[0m")
		self.draw_table(self.stored_dataframe)
