import nltk
import pandas as pd

noticias = pd.read_excel('data/Ibex35Noticias.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in data.values()]

