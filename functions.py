END_OF_LINE = "\n"
EMPTY_LINE = "\n\n"

def creerGraphe(fileName):
    
    hasChargingDock = dict()
    CLSC = dict()

    file = open(fileName,"r").read()
    
    bornesCLSC,noeuds = file.split(EMPTY_LINE)

    listBornes = bornesCLSC.split(END_OF_LINE)
    listNoeuds = noeuds.split(END_OF_LINE)

    for line in listBornes:
        numero, hasCharge = line.split(',')
        hasChargingDock[numero] = hasCharge

    for line in listNoeuds:
        nodeA, nodeB, cost = line.split(',')
        
        if nodeA not in CLSC:
            CLSC[nodeA] = {}
        if nodeB not in CLSC:
            CLSC[nodeB] = {}
        
        CLSC[nodeA][nodeB] = cost
        CLSC[nodeB][nodeA] = cost
        

        
    return hasChargingDock,CLSC