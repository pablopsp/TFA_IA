import pandas as pd

data = pd.read_excel('data/Ibex35Data.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in data.values()]

