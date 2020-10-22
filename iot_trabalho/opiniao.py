"""
    Biblioteca de manipulação de opiniões
"""

__all__ = ("Opiniao", "consenso")

import typing as T
from dataclasses import dataclass
from termcolor import colored, cprint

# from sympy import symbols, limit


DIV = 1


@dataclass
class Opiniao:
    """
    Cada objeto define uma opinião de uma determinada fonte (tido como
    um "indivíduo" ind) acerca de um determinado evento (ev). Uma opinião
    contém parâmetros de crença (b), descrença (d) e incerteza (u)
    """

    fonte: str
    evento: T.Any  # Ajustar esse tipo aqui, não sei qual é ainda
    crenca: float = 0.0
    descrenca: float = 0.0
    incerteza: float = 1.0


def consenso(w_a: Opiniao, w_b: Opiniao, lim: float = 0.0001) -> Opiniao:
    """Computa o consenso entre duas opiniões de diferentes fontes
    acerca de um mesmo evento"""

    if w_a.evento != w_b.evento:
        cprint(
            "WARNING:\t Opiniões dizem respeito a eventos diferentes. Resultado "
            "pode não ter sentido prático",
            "yellow",
        )

    if w_a.fonte == w_b.fonte:
        cprint("WARNING:\t Ambas as opinões são oriundas da mesma fonte", "yellow")

    # Combinação das opiniões
    w_ab = Opiniao(f"{w_a.fonte}+{w_b.fonte}", w_a.evento)

    divisor = w_a.incerteza + w_b.incerteza - (w_a.incerteza * w_b.incerteza)

    if abs(divisor) > lim:
        w_ab.crenca = (
            (w_a.crenca * w_b.incerteza) + (w_b.crenca * w_a.incerteza)
        ) / divisor
        w_ab.descrenca = (
            (w_a.descrenca * w_b.incerteza) + (w_b.descrenca * w_a.incerteza)
        ) / divisor
        w_ab.incerteza = (w_b.incerteza * w_a.incerteza) / divisor

    else:
        div = DIV  # w_b.incerteza/w_a.incerteza
        w_ab.crenca = (div * w_b.crenca + w_a.crenca) / (div + 1)
        w_ab.descrenca = (div * w_b.descrenca + w_a.descrenca) / (div + 1)
        w_ab.incerteza = 0
        # FIXME: Nao sei se essas contas estao certas!

    return w_ab
