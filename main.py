from menu import menu

def main():
    hasChargingDock, GrapheCLSCs = creerGraphe("centresLocaux.txt")
    
    #result = plusCourtChemin('haut_risque','23','20')
    result2 = extraireSousGraphe('haut_risque', '23')
    print (result2)

    #lireGraphe(GrapheCLSCs)
    #print (batterie)
    #print(Vehicule.NINH)
    
    
main()