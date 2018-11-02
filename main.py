from menu import *

def main():
<<<<<<< HEAD
    creerGraphe("centresLocaux.txt")
    #a = extraireSousGraphe(Risque.haut, "2", Vehicule.NI_MH)
    #b = testLongChemin("2", 100)
    #print(a)
    #print(b)

    for x in range(1,30):
        for vehicule in Vehicule:
            for risque in Risque:
                print(str(x) + " : " + str(vehicule) + " : " + str(risque))
                a = extraireSousGraphe(risque, str(x), vehicule)
                print (a)
=======
    menu()
    
>>>>>>> 8676c76981a2bdba4d1b418813f29fbb1663c902
main()