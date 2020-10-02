# -*- coding: utf-8 -*-

import pandas as pd
import requests 

# Formato da data: AAAA-MM-DD
datai = '2020-07-26'
dataf = '2020-07-27'
est_cod = 'A621'

url = 'https://apitempo.inmet.gov.br/estacao/' + datai + '/' + dataf + '/' + est_cod
r = requests.get(url)
info = r.json()
# print(info[0])

df = pd.DataFrame(info)
df.to_csv('inmet_teste.csv')