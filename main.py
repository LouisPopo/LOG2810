from graphesFunctions import creerGraphe, lireGraphe, plusCourtChemin
from menu import menu
from Test import PlusCourtCheminTest

GrapheCLSCs = None

fakeDict = {
    '1' : {'2':1,'4':3},
    '2' : {'1':1,'3':5,'5':4},
    '3' : {'2':2, '4':3},
    '4' : {'1':3,'5':4},
    '5' : {'2':4,'4':4}
}

    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    #lireGraphe(GrapheCLSCs)
    #plusCourtChemin()
    #menu()
    PlusCourtCheminTest(GrapheCLSCs)
    

    
main()