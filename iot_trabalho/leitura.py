"""
    Biblioteca de leitura de dados
"""

__all__ = ['load_dados']

import pandas as pd
import numpy as np



def abre_dados(nome_csv):
    # TODO: Modificar para quando as estações já vêm com informação apenas diária
    #   Acrescentar nomes das estações??? Poderia ser melhor do que código...

    # nome_csv: string com o nome do arquivo csv
    # Nota: a data da medição já é o index!!!
    # Ex: ['CD_ESTACAO','TEM_INS','TEM_MAX','TEM_MIN']

    # abre o arquivo csv:
    # path_dados = 'IoT-trabalho/dados/'
    path_dados = 'dados/'
    df = pd.read_csv(path_dados + nome_csv, index_col=0, encoding='latin')

    df.drop('HR_MEDICAO', axis=1, inplace=True)

    # Define a data da medição como index:
    df.set_index('DT_MEDICAO', inplace=True)

    # formata data:
    df = df.groupby('DT_MEDICAO').agg({'TEM_MAX': 'max', 'TEM_MIN': 'min', 'DC_NOME': 'min'})

    # seleciona as colunas desejadas:
    df = df[['TEM_MAX','TEM_MIN','DC_NOME']]

    return df


def load_dados(est_cod):
    for est in est_cod:
        df = abre_dados(est+'_2020-03.csv')
        nome = df['DC_NOME']
        df.drop('DC_NOME', axis=1, inplace=True)
        dfMin = df
        dfMax = df.copy()
        dfMin[nome] = dfMin['TEM_MIN']
        dfMax[nome] = dfMax['TEM_MAX']
        dfMin.drop(dfMin.columns[0:2], axis=1, inplace=True)
        dfMax.drop(dfMax.columns[0:2], axis=1, inplace=True)
        try:
            df_comp_dia_min = pd.concat([df_comp_dia_min, dfMin], axis=1)
            df_comp_dia_max = pd.concat([df_comp_dia_max, dfMax], axis=1)
        except:
            df_comp_dia_min = dfMin
            df_comp_dia_max = dfMax

    return df_comp_dia_min, df_comp_dia_max


def teste():
    cd_estacoes = ['A621', 'A618', 'A606', 'A609', 'A607']

    def_min, df_max = load_dados(cd_estacoes)

    print(df_max.head(10))


def get_dados():
    """
        A cada chamada desse gerador a função retorna a próxima leitura dos dados
    :return:
    """
    # TODO
    pass
