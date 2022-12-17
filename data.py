#Libraries for smart search
#!Should add annotation to each one
import nltk #Natural Language Toolkit - library for Natural Language Processing
from nltk.corpus import stopwords #Package of nltk to read corpus files
from pymorphy2 import MorphAnalyzer #Morphological analyzer for the Russian language
from sklearn.feature_extraction.text import TfidfVectorizer #Machine learning library
import pandas as pd


nltk.download('stopwords') #downloading stopwords list (words with little meaning)
stopwords_ru = stopwords.words('russian')

morph = MorphAnalyzer() #Object of class MorphAnalyzer to determine russian words characteristics

tfidf = TfidfVectorizer() #Object of class TfidfVectorizer to convert text to word frequency vectors
df = pd.read_csv("data_tables/without_str_SHORT.csv")
tfidf_features = tfidf.fit_transform(df['tokenz']) #Returns matrix of features

class Data():
	def __init__(self, parent):
		pass
		#self.data_table.pack()