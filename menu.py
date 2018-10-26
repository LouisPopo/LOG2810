def Affichage():
    print(
    '''
    **************************************************
    *                    Choix:                      *
    **************************************************
    * a) Mettre à jour la carte                      *
    * b) Déterminer le plus court chemin sécuritaire *
    * c) Extraire un sous-graphe                     *
    * d) Quitter                                     *
    **************************************************
    '''
    )


def MiseAJour():
    print("miseajour")
    menu()

def CheminPlusCourtSecuritaire():
    print("chemin")
    menu()

def ExtraireSousGraphe():
    print("soous")
    menu()

def Quitter():
    print("Fin du programme")
    return 0

def menu():
    options = {'a' : MiseAJour,
                'b' : CheminPlusCourtSecuritaire,
                'c' : ExtraireSousGraphe,
                'd' : Quitter,
    }
    Affichage()
    choix = input("Veuillez entrer un option (a, b, c ou d): ")
    if choix in options:
        print("Vous avez entré: " + choix)
        options[choix]()
    else:
        print("Cette option n'existe pas. Veuillez choisir l'une des option possible: ")
        menu()