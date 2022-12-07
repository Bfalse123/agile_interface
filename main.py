import nltk
from nltk.corpus import stopwords
import pandas as pd
from pymorphy2 import MorphAnalyzer
from razdel import tokenize, sentenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
stopwords_ru = stopwords.words('russian')
morph = MorphAnalyzer()
tfidf = TfidfVectorizer()
df = pd.read_csv('/home/viktor/agile_project/without_str.csv')
tfidf_features = tfidf.fit_transform(df['tokenz'])

def main():
    pass


if __name__ == "__main__":
    main()
