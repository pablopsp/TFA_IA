# -*- coding: utf-8 -*-
"""
@author: Pablo
"""
import requests
import pandas as pd

from bs4 import BeautifulSoup    

    
def GetDataOfIndex35From_Bolsamadrid():
    data = []
    
    main_page = requests.get('http://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000').text
    soup = BeautifulSoup(main_page, 'lxml')
    tabla_empresas = soup.find('table', {'id': 'ctl00_Contenido_tblAcciones'})
        
    for link in tabla_empresas.find_all('a'):
        each_page = requests.get('http://www.bolsamadrid.es' + link['href']).text
        each_soup = BeautifulSoup(each_page, 'lxml')
        div_links = each_soup.find('div', {'class': 'SubMenu noimpr'}).find_all('a', href = True)
        
        for link in div_links:
            if 'InfHistorica' in (link['href']):    
                df = pd.DataFrame(columns=('Fecha','Cierre','Referencia','Volumen','Efectivo','Último','Máximo','Mínimo','Medio'))
                
                data_page = requests.get('http://www.bolsamadrid.es' + link['href']).text
                data_soup = BeautifulSoup(data_page, 'lxml')
                table_data_soup = data_soup.find('table', {'id': 'ctl00_Contenido_tblDatos'})
                
                for tr in table_data_soup.findChildren(['tr'])[1:]:
                     eachTr_tdData = [i.text for i in tr.find_all('td')]
                     df.loc[len(df)] = eachTr_tdData
                     
                brand_name = data_soup.find('th', {'class': 'Ult'}).find_all('a', href = True)[0].string
                data.append({'brand': brand_name, 'data': df.values.tolist()})
                
                break

    writer = pd.ExcelWriter('Ibex35Data.xlsx', engine = 'xlsxwriter')
    for company in (companies for companies in data):
        df = pd.DataFrame(company['data'])
        df.columns = ['Fecha','Cierre','Referencia','Volumen','Efectivo','Último','Máximo','Mínimo','Medio']
        df.to_excel(writer, sheet_name = company['brand'].split(',')[0][:30])
    
    writer.save()
    
    return data 