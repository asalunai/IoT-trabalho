#!/usr/bin/env python3

from pathlib import Path

import simpy

from iot_trabalho.receptor import *  # Receptor
from .leitura import DataReader


def main() -> None:
    print("Hello World")

    # env = simpy.Environment()
    # N = 5
    # waitTime = 5
    #
    # r1 = Receptor('r1', env, N, waitTime)
    #
    #
    #
    # env.run(until=10)

    reader = DataReader(
        Path("./dados_diarios"),
        [
            "A606",
            "A607",
            "A609",
            "A618",
            "A621",
        ],
    )

    for entry in reader.read_day_by_day():
        print(entry)


if __name__ == "__main__":
    main()
