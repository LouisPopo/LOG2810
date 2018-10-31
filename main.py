from menu import menu
from graphesFunctions import *

def main():
    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    
    #result = plusCourtChemin('haut_risque','23','20')
    result2 = extraireSousGraphe('faible_risque', '23')
    print (result2)

    #lireGraphe(GrapheCLSCs)
    #print (batterie)
    #print(Vehicule.NINH)
    
    
main()