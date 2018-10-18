BREAK_LINE = "\n"
EMPTY_LINE = "\n\n"

def readFile(file):
    
    hasChargingDock = dict()
    CLSC = dict()


    f = open(file,"r").read()
    
    bornesCLSC,noeuds = f.split(EMPTY_LINE)

    listBornes = bornesCLSC.split(BREAK_LINE)
    listNoeuds = noeuds.split(BREAK_LINE)

    for line in listBornes:
        numero, hasCharge = line.split(',')
        CLSC[numero] = hasCharge

    for line in listNoeuds:
        # remplir dictionnaire CLSC


    return (hasChargingDock,CLSC)