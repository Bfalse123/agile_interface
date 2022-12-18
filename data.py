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
from tkinter import ttk #Exension for tkinter themed widgets

import re #Library for regexes
import numpy as np #Library to work with arrays and matrixes


# Downloading stopwords list (words with little meaning)
nltk.download('stopwords')
stopwords_ru = stopwords.words('russian')

# Object of class MorphAnalyzer to determine russian words characteristics
morph = MorphAnalyzer()

# Object of class TfidfVectorizer to convert text to word frequency vectors
tfidf = TfidfVectorizer()

df = pd.read_csv("data_tables/test.csv")
tfidf_features = tfidf.fit_transform(df["tokenz"])  #Returns matrix of features

class Data():
	"""
Representation of data class
	"""
	def __init__(self, parent):
		self.table = ttk.Treeview(parent)

		# create scroll objects
		self.scroll_Y = tk.Scrollbar(self.table, orient=tk.VERTICAL, command=self.table.yview)
		self.scroll_X = tk.Scrollbar(self.table, orient=tk.HORIZONTAL, command=self.table.xview)
		
		self.table.configure(yscrollcommand=self.scroll_Y.set, xscrollcommand=self.scroll_X.set)
		
		self.scroll_Y.pack(side=tk.RIGHT, fill=tk.Y)
		self.scroll_X.pack(side=tk.BOTTOM, fill=tk.X)
		self.table.place(rely=0.08, relx=0.17, relwidth=0.9, relheight=0.95) #!!!!!!!!

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
		
		return None
	

	def tokens(self, entry):
		lst = list(tokenize(entry))
		s = ''
		for i in lst:
			if i.text and i.text not in stopwords_ru:
				s += (morph.normal_forms(i.text)[0] + ' ')
				s = re.sub(r'\| |\ \)| \(| \:', '', s)
		return s

	def tff(self, queary):
		"""
		Extract descriptions from file
		"""
		q_tokens = self.tokens(queary)
		q_tokens = q_tokens.split()
		q_transform = tfidf.transform(q_tokens)

		cosine_dist = cosine_distances(tfidf_features, q_transform)[:, 0]
		indices = np.argsort(cosine_dist.flatten())[0:10]
		df_indices = list(df['tokenz'].index[indices])

		return df.tokenz[df_indices[:]]

	def find_value(self, keys):
		spisok_rec = self.tff(keys).index
		new_df = self.stored_dataframe
		df_rec = pd.DataFrame(
			columns=new_df.columns,
			index=[
				'rec_' +
				str(i) for i in range(
					len(spisok_rec))])

		for j in range(len(spisok_rec)):
			df_rec.loc['rec_' + str(j)] = new_df.iloc[spisok_rec[j]]

		self._draw_table(df_rec)

	def reset_table(self):
		self._draw_table(self.stored_dataframe)
