#!/usr/bin/env python3

from pathlib import Path

import simpy

from iot_trabalho.receptor import *  # Receptor
from .leitura import DataReader


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



    env.run(until=10)

    #for entry in reader.read_day_by_day():
    #    print(entry)


if __name__ == "__main__":
    main()
