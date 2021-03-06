import requests
import pandas as pd
import time
import json

from threading import Thread
from bs4 import BeautifulSoup

domain = 'https://www.eleconomista.es'

#devuelve una list de urls pasandole el valor del url del indice bursatil que se quiera
def GetUrlsFrom(indiceBursatil):
    companies_page = requests.get('https://www.eleconomista.es/indice/' + indiceBursatil).text
    soup = BeautifulSoup(companies_page, 'lxml')
    companies = soup.find_all('td', {'class' : 'footable-first-visible'})
    return companies

#devuelve toda la data de las tablas de cada compañia y las guarda en una lis(dict(string, list))
#si quieres sacar mas o menos valores solo hay que cambiar el valor de la i en el while
data = []
def GetData(companie):
    link = companie.find('a')['href']
    print("scrapping data from: " + link)
    url = domain + link + '/historico'
    each_page = requests.get(url).text
    each_soup = BeautifulSoup(each_page, 'lxml')   
    
    df = pd.DataFrame(columns=('Fecha','Cierre','Var.(€)','Var.(%)','Máx','Mín','Volumen(€)'))
    
    i=0
    while i < 270:
        for table in each_soup.find_all('tbody'):    
            for tr in table.findChildren(['tr']):
                eachTr_tdData = [i.text for i in tr.find_all('td')][0:7]
                df.loc[len(df)] = eachTr_tdData
                                 
        each_soup = BeautifulSoup(requests.get(domain + each_soup.find('a', {'class':'page-link'})['href']).text, 'lxml')
        i = i+1
        
    data.append({'brand': each_soup.find('h1').text, 'data': df.values.tolist()})
    data.sort(key=lambda companie: companie['brand'])


#mete todos los valores de data 'lis(dict(string, list))' en un excell
def ToExcell():
    writer = pd.ExcelWriter('data/Ibex35Data.xlsx', engine = 'xlsxwriter')

    for company in (companies for companies in data):
        df = pd.DataFrame(company['data'])
        df.columns = ['Fecha','Cierre','Var.(€)','Var.(%)','Máx','Mín','Volumen(€)']
        df.to_excel(writer, sheet_name = company['brand'].split(',')[0][:30])
    writer.save()


def ToJSON():
    with open('data/Ibex35Data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)
        
#main function, con threads para que tarde menos +- 25 minutos con 270 valores de i
def main():
    start_time = time.time()
    threadlist = []
    for companie in GetUrlsFrom("Ibex-35"):
        t = Thread(target=GetData, args =(companie,))
        t.start()
        threadlist.append(t)    
    [thread.join() for thread in threadlist]
    
    ToExcell()
    ToJSON()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()