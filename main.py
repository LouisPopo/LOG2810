from graphesFunctions import creerGraphe, lireGraphe, plusCourtChemin
from menu import menu
from Test import PlusCourtCheminTest

GrapheCLSCs = None

def main():


    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    #lireGraphe(GrapheCLSCs)
    #plusCourtChemin()
    #menu()
    PlusCourtCheminTest(GrapheCLSCs)
    

main()