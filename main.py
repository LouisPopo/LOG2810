from graphesFunctions import *
from menu import menu
from dictionnaires import *

GrapheCLSCs = None

fakeDict = {
    'A' : {'B':3,'C':2},
    'B' : {'A':3,'C':6,'F':4},
    'C' : {'A':5, 'B':3,'F':8},
    'D' : {'F':12},
    'E' : {'B':4,'D':1}
}

def main():
    creerGraphe("centresLocaux.txt")
    
    #resultat = plusCourtChemin(Risque.haut, '23', '27')

    a = extraireSousGraphe(Risque.faible, "28", Vehicule.LI_ion)
    print(a)

main()