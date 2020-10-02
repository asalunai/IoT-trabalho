# -*- coding: utf-8 -*-

import pandas as pd
import requests 

# Formato da data: AAAA-MM-DD
datai = '2020-10-01'
dataf = '2020-10-02'
est_cod = ['A621', 'A618', 'A606', 'A609', 'A607']
nomes = ['Vila Militar', 'Teresópolis', 'Cabo Frio', 'Resende', 'Campos dos Goytacazes']

for est in est_cod:
    url = 'https://apitempo.inmet.gov.br/estacao/' + datai + '/' + dataf + '/' + est
    print(url)
    r = requests.get(url)
    info = r.json()
    # print(info[0])

    df = pd.DataFrame(info)
    df.to_csv(est+'_'+datai[:-2]+'.csv')