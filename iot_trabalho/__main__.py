#!/usr/bin/env python3

from pathlib import Path

import simpy
import numpy as np
import typing as T
from dataclasses import dataclass, field
import csv
from collections import deque

from receptor import *  # Receptor
from leitura import DataReader


N_DADOS = 10

out_files = [
    [
        "dados_csv/media_9est.csv",
        "dados_csv/crenca_9est.csv",
        "dados_csv/descrenca_9est.csv",
        "dados_csv/incerteza_9est.csv",
        "dados_csv/anomalia_9est.csv",
    ],
]


@dataclass
class Coordenador:
    nome: str
    receptores: T.List[Receptor]
    env: simpy.Environment

    wait: float = 1

    def __post_init__(self):
        self.medias = [
            deque() for _ in range(len(self.receptores))
        ]  # TODO: Mudar tipo. Como organizar os dados recebidos dos receptores?
        self.crencas = np.zeros((N_DADOS, len(self.receptores)))
        self.descrencas = np.zeros((N_DADOS, len(self.receptores)))
        self.incertezas = np.zeros((N_DADOS, len(self.receptores)))
        self.anomalia = np.zeros((N_DADOS, len(self.receptores)))  # TODO: anomalias?
        self.limiar = 10.0
        self.action = self.env.process(self.run())

    def run(self):
        while True:
            # TODO: Incialmente printar grafos. Mas a ideia é fazer analise
            ## Salvando dados em csv (para gerar gráficos)
            # for idx, name in enumerate(out_files):
            #    with open(name, 'a', newline='') as f:
            #        writer = csv.writer(f, delimiter=',')
            #        writer.writerow(data_l[idx])

            # print(data_l)
            for i, r in enumerate(self.receptores):
                # self.medias[-1, i], self.crencas[-1, i], self.descrencas[-1, i], self.incertezas[-1, i], self.anomalia[-1, i] = r.get_data()
                data_l = list(r.get_data())
                self.medias[i].append(data_l[0])
                if len(self.medias[i]) > N_DADOS:
                    self.medias[i].popleft()

                ## Salvando dados em csv (para gerar gráficos)
                for idx, name in enumerate(out_files[i]):
                    with open(name, "a", newline="") as f:
                        writer = csv.writer(f, delimiter=",")
                        writer.writerow(data_l[idx] if idx != 0 else [data_l[idx]])

                # print(data_l)

            max_temps = []
            min_temps = []
            for medias in self.medias:
                max_temps.append(max(medias))
                min_temps.append(min(medias))

            frentes_frias = [
                max_temp - min_temp > self.limiar
                for max_temp, min_temp in zip(max_temps, min_temps)
            ]
            for receptor, frente_fria in enumerate(frentes_frias):
                if frente_fria:
                    print(f"Frente fria detectada no receptor {receptor}: ")

            for i in range(len(self.receptores)):
                with open(f"dados_csv/frentes_frias_{i + 1}-{self.receptores[i].nome}.csv", "a", newline="") as f:
                    f.write(f"{max_temps[i]},{min_temps[i]},{frentes_frias[i]}\n")

            yield self.env.timeout(self.wait)


def main() -> None:
    sensoresTot = [ 'A899','A806','A873','A834','A712','A619','A606','A620' ]

    env = simpy.Environment()

    readerTot = DataReader(
        Path("./dados_diarios"),
        sensoresTot,
    )

    N = len(sensoresTot)

    r1 = Receptor("rTot", env, N, readerTot)

    c = Coordenador("c", [r1], env)

    env.run(until=397)  # Temos 397 dias

    # for entry in reader.read_day_by_day():
    #    print(entry)


if __name__ == "__main__":
    main()
