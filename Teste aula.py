import numpy as np
import pandas as pd
import random as rd
from sklearn.model_selection import train_test_split

dados = pd.read_csv('dados_renda_municipios.csv')

#print(dados.head())
#print(dados.shape)

#Amostragem por estado
uf = 'São Paulo'
dados_municipio = dados[dados['UF'] == uf]
#print(dados_municipio.shape)

#Criação de estratos
dados_municipio['classe_renda'] = pd.qcut(dados_municipio['RDPC'], 4, labels = ['D', 'C', 'B', 'A'])
#print(dados_municipio.head())

#dados amostra piloto
dados_piloto = dados_municipio.agg(media_RDPC = pd.NamedAgg('RDPC', 'mean'),
                                   dp_RDPC = pd.NamedAgg('RDPC', 'std'),
                                   N = pd.NamedAgg('RDPC', 'count'))
print(dados_piloto)

dados_piloto_classe = dados_municipio.groupby('classe_renda')\
                                     .agg(media_RDPC = pd.NamedAgg('RDPC', 'mean'),
                                          dp_RDPC = pd.NamedAgg('RDPC', 'std'),
                                          N = pd.NamedAgg('RDPC', 'count'))

print(dados_piloto_classe)