#Libraries for smart search
#!Should add annotation to each one
import nltk #Natural Language Toolkit - library for Natural Language Processing
from nltk.corpus import stopwords #Package of nltk to read corpus files
from pymorphy2 import MorphAnalyzer #Morphological analyzer for the Russian language
from sklearn.feature_extraction.text import TfidfVectorizer #Machine learning library
import pandas as pd

from tkinter import ttk
import tkinter as tk
import re

nltk.download('stopwords') #downloading stopwords list (words with little meaning)
stopwords_ru = stopwords.words('russian')

morph = MorphAnalyzer() #Object of class MorphAnalyzer to determine russian words characteristics

tfidf = TfidfVectorizer() #Object of class TfidfVectorizer to convert text to word frequency vectors
df = pd.read_csv("data_tables/without_str_SHORT.csv")
tfidf_features = tfidf.fit_transform(df['tokenz']) #Returns matrix of features

class Data(ttk.Treeview):
	"""
	Representation of data class
	"""
	def __init__(self, parent):
		super().__init__(parent)
		scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
		scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
		self.configure(
            yscrollcommand=scroll_Y.set,
            xscrollcommand=scroll_X.set)
		scroll_Y.pack(side="right", fill="y")
		scroll_X.pack(side="bottom", fill="x")
		self.stored_dataframe = pd.DataFrame()
	

	def set_datatable(self, dataframe):
		self.stored_dataframe = dataframe
		self._draw_table(dataframe)
	

	def _draw_table(self, dataframe):
		self.delete(*self.get_children())
		columns = list(dataframe.columns)
		
		self.__setitem__("column", columns)
		self.__setitem__("show", "headings")
		for col in columns:
			self.heading(col, text=col)
			
		df_rows = dataframe.to_numpy().tolist()
		for row in df_rows:
			self.insert("", "end", values=row)
	

	def tokens(self, entry):
		lst = list(tokenize(entry))
		s = ''
		for i in lst:
			if i.text and i.text not in stopwords_ru:
				s += (morph.normal_forms(i.text)[0] + ' ')
				s = re.sub(r'\| |\ \)| \(| \:', '', s)
		return s
	

	