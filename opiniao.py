"""
    Biblioteca de manipulação de opiniões
"""

__all__ = ['Opiniao',
           'consenso']

from termcolor import colored, cprint
# from sympy import symbols, limit



class Opiniao:
    def __init__(self, ind, ev, b=0, d=0, u=1):
        """
            Cada objeto define uma opinião de uma determinada fonte (tido como
            um "indivíduo" ind) acerca de um determinado evento (ev). Uma opinião
            contém parâmetros de crença (b), descrença (d) e incerteza (u)
        """
        self.fonte = ind
        self.evento = ev
        self.crenca = b
        self.descrenca = d
        self.incerteza = u


def consenso(w_a, w_b):
    """Computa o consenso entre duas opiniões de diferentes fontes
       acerca de um mesmo evento"""

    if not (isinstance(w_a, Opiniao) and isinstance(w_b, Opiniao)):
        raise BaseException(colored("ERROR:\t Argumentos inválidos. Precisam ser objetos 'Opiniao'", "red"))

    if w_a.evento != w_b.evento:
        cprint("WARNING:\t Opinões dizem respeiro a eventos diferentes. Resultado "
               "pode não ter sentido prático", "yellow")

    if w_a.fonte == w_b.fonte:
        cprint("WARNING:\t Ambas as opinões são oriundas da mesma fonte", "yellow")


    # Combinação das opiniões
    w_ab = Opiniao("{}+{}".format(w_a.fonte, w_b.fonte),
                   w_a.evento)

    divisor = w_a.incerteza + w_b.incerteza - (w_a.incerteza * w_b.incerteza)

    if divisor != 0:
        w_ab.crenca = ( (w_a.crenca * w_b.incerteza) + (w_b.crenca * w_a.incerteza) )/divisor
        w_ab.descrenca = ( (w_a.descrenca * w_b.incerteza) + (w_b.descrenca * w_a.incerteza) )/divisor
        w_ab.incerteza = ( w_b.incerteza * w_a.incerteza )/divisor

    # TODO: Nao entedi como faz o limite...
    #else:
    #    gamma_a =

    return w_ab