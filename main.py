from graphesFunctions import creerGraphe, lireGraphe, plusCourtChemin
<<<<<<< HEAD
from menu import menu
from Test import PlusCourtCheminTest
=======
>>>>>>> 22276de2c98608efd11163e39722882d260055cf

GrapheCLSCs = None

fakeDict = {
    '1' : {'2':1,'4':3},
    '2' : {'1':1,'3':5,'5':4},
    '3' : {'2':2, '4':3},
    '4' : {'1':3,'5':4},
    '5' : {'2':4,'4':4}
}

<<<<<<< HEAD
    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    #lireGraphe(GrapheCLSCs)
    #plusCourtChemin()
    #menu()
    PlusCourtCheminTest(GrapheCLSCs)
    
=======
def main():
    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    #lireGraphe(GrapheCLSCs)
    plusCourtChemin(fakeDict)
>>>>>>> 22276de2c98608efd11163e39722882d260055cf

    
main()