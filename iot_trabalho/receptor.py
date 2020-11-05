"""
    Algoritmo para rodar no nó R (receptor)
    - Versão standalone (necessárias modificações para ajustar à simulação)
"""

__all__ = ["Receptor"]


from dataclasses import dataclass
import numpy as np
from simpy import Environment

from iot_trabalho.opiniao import *  # Opiniao, consenso
from iot_trabalho.leitura import *  # DataReader, DailyData

# from dados import get_dados


# TODO:
#   - Testar
#   - Mesclar com a implementação


# ------------


def anomalia(dado: float, media: float, desvio: float) -> bool:
    # TODO: Rever essa definicao de anomalia
    return abs(dado - media) > 1.5*desvio


def media_seletiva(arr: np.ndarray, indices) -> float:
    # FIXME: indices should be 'dict_keys' type, mas nao reconhece
    som = 0.0
    tot = 0
    idx = 0
    for v in arr:
        if not idx in indices:
            som += v
            tot += 1
        idx += 1
    return som / tot


@dataclass
class Receptor:
    nome: str
    env: Environment
    N: int  # Número de sensores conectados ao nó
    reader: DataReader

    wait: float = 1  # Número de iterações a se esperar
    # TODO: Mudar essa variavel. Por enquanto estou considerando unidade 'dias' (espera 1 dia para analisar de novo.

    p: float = 1  # Peso dos eventos positivos
    n: float = 10  # Peso dos eventos negativos
    MIN: float = (
        0.001  # Menor valor antes de uma opinião ser consederada dogmática (constante)
    )

    b0: float = 0
    d0: float = 0
    u0: float = 1

    def __post_init__(self):
        # TODO: Verificar como organizar as variaveis, quais devem ser atributos...
        self.eventos = {"positivos": np.zeros(self.N), "negativos": np.zeros(self.N)}
        # self.dados = np.zeros(self.N)
        self.opTot = [
            Opiniao(str(i), "all", self.b0, self.d0, self.u0) for i in range(self.N)
        ]
        self.opNow = [Opiniao(str(i), 0) for i in range(self.N)]

        self.k = 1

        self.reader = self.reader.read_day_by_day()

        self.action = self.env.process(self.run())

    def run(self):
        while True:
            dictDados = next(self.reader)
            # TODO: Discutir os dados que vamos usar, e COMO vamos usar aqui dentro

            dados = np.zeros(self.N)
            i = 0
            soma = 0
            for totalInfo in dictDados.values():
                dados[i] = totalInfo.max_temp
                soma += totalInfo.max_temp
                i += 1

            #print(dictDados.values())

            media = soma/i
            dp = dados.std()

            anomaliasAtuais = {}

            for i in range(self.N):
                if anomalia(dados[i], media, dp):  # Caso de anomalia
                    self.eventos["negativos"][i] += self.n
                    anomaliasAtuais[i] = dados[i]
                else:
                    self.eventos["positivos"][i] += self.p

                b = self.eventos["positivos"][i] / (
                    self.eventos["positivos"][i] + self.eventos["negativos"][i] + self.k
                )
                d = self.eventos["negativos"][i] / (
                    self.eventos["positivos"][i] + self.eventos["negativos"][i] + self.k
                )
                u = self.k / (
                    self.eventos["positivos"][i] + self.eventos["negativos"][i] + self.k
                )

                self.opNow[i] = Opiniao(str(i), self.env.now, b, d, u)

                self.opTot[i] = consenso(self.opTot[i], self.opNow[i])

            if anomaliasAtuais:
                media = media_seletiva(dados, anomaliasAtuais.keys())

            self.send_data(media, anomaliasAtuais)

            yield self.env.timeout(self.wait)

    def send_data(self, mean: float, currAnom: dict = {}):
        # TODO: Como eviar essa informação? pra quem enviar?

        # Temporariamente, para teste, está sendo apenas impressa
        if currAnom:
            print(f"Iteração {self.env.now}: \n\t Media: {mean}\n\t Opinioes: {self.opTot}"
                  f"\n\tAnomalias: {currAnom}\n")
        else:
            print(f"Iteração {self.env.now}: \n\t Media: {mean}\n\t Opinioes: {self.opTot}\n")
