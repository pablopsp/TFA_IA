import requests
import pandas as pd
import time

from threading import Thread
from bs4 import BeautifulSoup


def GetUrlsFrom(indiceBursatil):
    companies_page = requests.get('https://www.eleconomista.es/indice/' + indiceBursatil).text
    soup = BeautifulSoup(companies_page, 'lxml')
    companies = soup.find_all('td', {'class' : 'footable-first-visible'})
    return companies

data = []
def GetData(companie):
    link = companie.find('a')['href']
    print("scrapping data from: " + link)
    url = 'https://www.eleconomista.es' + link + '/historico'
    each_page = requests.get(url).text
    each_soup = BeautifulSoup(each_page, 'lxml')   
    
    df = pd.DataFrame(columns=('Fecha','Cierre','Var.(€)','Var.(%)','Máx','Mín','Volumen(€)'))

    i=0
    while i < 35:
        for table in each_soup.find_all('tbody'):    
            for tr in table.findChildren(['tr']):
                eachTr_tdData = [i.text for i in tr.find_all('td')][0:7]
                df.loc[len(df)] = eachTr_tdData
        
        each_soup = BeautifulSoup(requests.get('https://www.eleconomista.es' + each_soup.find('a', {'class':'page-link'})['href']).text, 'lxml')
        i = i+1
        
    data.append({'brand': each_soup.find('h1').text, 'data': df.values.tolist()})

def ToExcell():
    writer = pd.ExcelWriter('Ibex35Data.xlsx', engine = 'xlsxwriter')
    for company in (companies for companies in data):
        df = pd.DataFrame(company['data'])
        df.columns = ['Fecha','Cierre','Var.(€)','Var.(%)','Máx','Mín','Volumen(€)']
        df.to_excel(writer, sheet_name = company['brand'].split(',')[0][:30])
    
    writer.save()


start_time = time.time()
threadlist = []
for companie in GetUrlsFrom("Ibex-35"):
    t = Thread(target=GetData, args =(companie,))
    t.start()
    threadlist.append(t)
    
[thread.join() for thread in threadlist]
print("--- %s seconds ---" % (time.time() - start_time))
