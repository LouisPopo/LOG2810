from graphesFunctions import *
from menu import menu
from dictionnaires import *

GrapheCLSCs = None


def main():
    creerGraphe("centresLocaux.txt")
    a = extraireSousGraphe(Risque.faible, '1' ,Vehicule.LI_ion)
    print(a)


main()