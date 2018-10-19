from graphesFunctions import creerGraphe, lireGraphe, plusCourtChemin

GrapheCLSCs = None

def main():
    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    #lireGraphe(GrapheCLSCs)
    plusCourtChemin()
    

main()