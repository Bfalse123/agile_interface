#Libraries for smart search
#!Should add annotation to each one
import nltk #Natural Language Toolkit - library for Natural Language Processing
from nltk.corpus import stopwords #Package of nltk to read corpus files
from pymorphy2 import MorphAnalyzer #Morphological analyzer for the Russian language
from sklearn.feature_extraction.text import TfidfVectorizer #Machine learning library
import pandas as pd

from tkinter import ttk
import tkinter as tk

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
	
	