"""
    Biblioteca de manipulação de opiniões
"""

__all__ = ("Opiniao", "consenso")

import typing as T
from dataclasses import dataclass
from termcolor import colored, cprint

# from sympy import symbols, limit


DIV = 1
imprecisao = 0.000001

@dataclass
class Opiniao:
    """
    Cada objeto define uma opinião de uma determinada fonte (tido como
    um "indivíduo" ind) acerca de um determinado evento (ev). Uma opinião
    contém parâmetros de crença (b), descrença (d) e incerteza (u)
    """

    __fonte: str
    __evento: T.Any  # Ajustar esse tipo aqui, não sei qual é ainda
    __crenca: float = 0.0
    __descrenca: float = 0.0
    __incerteza: float = 1.0

    def __post_init__(self):
        if not self.consistente(self.__crenca, self.__descrenca, self.__incerteza):
            cprint("WARNING:\t Valores de opinião inválidos. Revertido para default.", "yellow")
            self.__crenca = 0.0
            self.__descrenca = 0.0
            self.__incerteza = 1.0

    def consistente(self, b, d, u):
        if abs(b + d + u - 1) <= imprecisao:
            return True
        return False

    def get_opiniao(self):
        return self.__crenca, self.__descrenca, self.__incerteza

    def set_opiniao(self, b, d, u):
        if self.consistente(b,d,u):
            self.__crenca = b
            self.__descrenca = d
            self.__incerteza = u
        else:
            cprint("WARNING:\t Valores de opinião inválidos. Opinião não foi alterada.", "yellow")

    def get_evento(self):
        return self.__evento

    def get_fonte(self):
        return self.__fonte



def consenso(w_a: Opiniao, w_b: Opiniao, lim: float = imprecisao) -> Opiniao:
    """Computa o consenso entre duas opiniões de diferentes fontes
    acerca de um mesmo evento"""

    if w_a.get_evento() != w_b.get_evento():
        cprint(
            "WARNING:\t Opiniões dizem respeito a eventos diferentes. Resultado "
            "pode não ter sentido prático",
            "yellow",
        )

    if w_a.get_fonte() == w_b.get_fonte():
        cprint("WARNING:\t Ambas as opinões são oriundas da mesma fonte", "yellow")

    # Combinação das opiniões
    w_ab = Opiniao(f"{w_a.get_fonte()}+{w_b.get_fonte()}", w_a.get_evento())

    b_a, d_a, u_a = w_a.get_opiniao()
    b_b, d_b, u_b = w_b.get_opiniao()

    divisor = u_a + u_b - (u_a * u_b)

    if abs(divisor) > lim:
        b_ab = ((b_a * u_b) + (b_b * u_a)) / divisor
        d_ab = ((d_a * u_b) + (d_b * u_a)) / divisor
        u_ab = (u_b * u_a) / divisor

        w_ab.set_opiniao(b_ab, d_ab, u_ab)
    else:
        div = DIV  # w_b.incerteza/w_a.incerteza
        b_ab = (div * b_b + b_a) / (div + 1)
        d_ab = (div * d_b + d_a) / (div + 1)
        u_ab = 0
        # FIXME: Nao sei se essas contas estao certas!

        w_ab.set_opiniao(b_ab, d_ab, u_ab)

    return w_ab


def teste() -> None:
    wA = Opiniao('A', 1, 0.8, 0.1, 0.1)
    wB = Opiniao('B', 1, 0.7, 0.15, 0.15)

    print("wA: ", wA.get_opiniao())
    print("wB: ", wB.get_opiniao())
    print("wA + wB: ", consenso(wA, wB))

    wC = Opiniao('C', 2, 0.7, 0.1, 0.5)
    print(wC)

    print("wA + wC: ", consenso(wA, wC))
    print("wA + wA: ", consenso(wA,wA))