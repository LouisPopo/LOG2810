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
    #a = extraireSousGraphe(Risque.haut, "2", Vehicule.NI_MH)
    #b = testLongChemin("2", 100)
    #print(a)
    #print(b)

    for x in range(1,30):
        for vehicule in Vehicule:
            for risque in Risque:
                print(str(x) + " : " + str(vehicule) + " : " + str(risque))
                a = extraireSousGraphe(risque, str(x), vehicule)
                print (a)
main()