from graphesFunctions import *
from menu import menu
from dictionnaires import *

GrapheCLSCs = None

fakeDict = {
    'A' : {'B':3,'C':2},
    'B' : {'A':3,'C':6,'F':4},
    'C' : {'A':5, 'B':3,'F':8},
    'D' : {'F':12},
    'E' : {'B':4,'D':1}
}

def main():
    creerGraphe("centresLocaux.txt")

    results = open("results.txt", 'a')
    cheminsImpo = []
    nimhfaible = 0
    lionfaible = 0
    nimhmoyen = 0
    lioinmoyen = 0
    nimhhaut = 0
    lionhaut = 0
    for x in range(1,30):
        for y in range(1,30):
            a = plusCourtChemin(Risque.faible, str(x), str(y))
            b = plusCourtChemin(Risque.moyen, str(x), str(y))
            c = plusCourtChemin(Risque.haut, str(x), str(y))
            if a == None:
                cheminsImpo.append(a)
            if b == None:
                cheminsImpo.append(a)
            if b == None:
                cheminsImpo.append(a)
            
            if a['Vehicule'] == Vehicule.NI_MH:
                nimhfaible += 1
            
            if a['Vehicule'] == Vehicule.LI_ion:
                lionfaible += 1

            if b['Vehicule'] == Vehicule.NI_MH:
                nimhmoyen += 1
            
            if b['Vehicule'] == Vehicule.LI_ion:
                lionmoyen += 1

            if c['Vehicule'] == Vehicule.NI_MH:
                nimhhaut += 1
            
            if c['Vehicule'] == Vehicule.LI_ion:
                lionhaut += 1



            results.write("From " + str(x) + " to " + str(y) + " \n")
            results.write(str(a))
            results.write("\n")
            results.write(str(b))
            results.write("\n")
            results.write(str(c))
            results.write("\n")
            results.write("-----------------------------------------\n")

    results.write("Chemins Impossible : \n")
    for impo in cheminsImpo:
        results.write(str(impo))
    results.write("\nVehicules utilises : \n")
    results.write("\nNI-MH faible : ")
    results.write(str(nimhfaible))
    results.write("\nLI-ion faible : ")
    results.write(str(lionfaible))
    results.write("\nNI-MH moyen : ")
    results.write(str(nimhmoyen))
    results.write("\nLI-ion moyen : ")
    results.write(str(lioinmoyen))
    results.write("\nNI-MH haut : ")
    results.write(str(nimhhaut))
    results.write("\nLI-ion haut : ")
    results.write(str(lionhaut))
    
    results.close()

    
main()