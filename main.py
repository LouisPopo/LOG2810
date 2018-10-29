from menu import menu
from dictionnaires import *
from enum import Enum
from graphesFunctions import *

def main():
    
    creerGraphe('centresLocaux.txt')
    res = plusCourtChemin(Risque.faible,'1','15')
    print(res)
main()