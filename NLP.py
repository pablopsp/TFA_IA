import nltk
import pandas as pd
import re


noticias = pd.read_excel('data/Ibex35Noticias.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in noticias.values()]

for key, compData in noticias.items():
    freqs = []
    for x in compData['Texto']:
        pattern = re.compile(r'\W+')
        tokens = pattern.split(x)
        freq = nltk.FreqDist(tokens)
        freqs.append(pd.DataFrame(list(freq.items()), columns = ["Word","Frequency"]))
        
    compData['Frequencies'] = freqs

