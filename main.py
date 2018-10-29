from menu import menu

def main():
    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    chemin, temps, vehicule, batterie = plusCourtChemin('faible_risque','1','15')
    
    #lireGraphe(GrapheCLSCs)
    print (batterie)
    #print(Vehicule.NINH)
    
    
main()