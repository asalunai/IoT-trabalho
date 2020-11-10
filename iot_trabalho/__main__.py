#!/usr/bin/env python3

from pathlib import Path

import simpy
import numpy as np
import typing as T
from dataclasses import dataclass, field

from iot_trabalho.receptor import *  # Receptor
from .leitura import DataReader


N_DADOS = 10


@dataclass
class Coordenador:
    nome: str
    receptores: T.List[Receptor]
    env: simpy.Environment

    wait: float = 1

    def __post_init__(self):
        self.medias = np.zeros((N_DADOS, len(self.receptores)))     # TODO: Mudar tipo. Como organizar os dados recebidos dos receptores?
        self.crencas = np.zeros((N_DADOS, len(self.receptores)))
        self.descrencas = np.zeros((N_DADOS, len(self.receptores)))
        self.incertezas = np.zeros((N_DADOS, len(self.receptores)))
        self.anomalia = np.zeros((N_DADOS, len(self.receptores)))  # TODO: anomalias?

        self.action = self.env.process(self.run())

    def run(self):
        while True:
            # TODO: Incialmente printar grafos. Mas a ideia é fazer analise

            for i, r in enumerate(self.receptores):
                #self.medias[-1, i], self.crencas[-1, i], self.descrencas[-1, i], self.incertezas[-1, i], self.anomalia[-1, i] = r.get_data()
                print(r.get_data())

            # TODO: Analise

            # TODO: Shiftar
            #1 -> 0
            #2 -> 1

            yield self.env.timeout(self.wait)


def main() -> None:
    sensores = [
        "A606",
        "A607",
        "A609",
        "A618",
        "A621",
    ]

    env = simpy.Environment()

    reader = DataReader(
        Path("./dados_diarios"),
        sensores,
    )

    N = len(sensores)

    r1 = Receptor('r1', env, N, reader)

    c = Coordenador('c', [r1], env)

    env.run(until=10) # Temos 397 dias

    #for entry in reader.read_day_by_day():
    #    print(entry)


if __name__ == "__main__":
    main()
