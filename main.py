from functions import creerGraphe


def main():
    hasChargingDock, CLSC = creerGraphe("centresLocaux.txt")
    #print(hasChargingDock)
    #print(CLSC)

    for nodes in CLSC:
        print(nodes)
        print (CLSC[nodes])


main()