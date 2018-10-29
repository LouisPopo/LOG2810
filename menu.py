from graphesFunctions import creerGraphe, plusCourtChemin, lireGraphe
from enum import Enum


#TODO:  test pour chaque entré de l'utilisateur
#       faire fonctionner lireGraphe
#       controle de lerreur de creer graphe
#       changer input miseajour



#Global variable initializing the state of map
global hasMap
hasMap = None

class Transport(Enum):
    faible = 'faible_risque'
    moyen = 'moyen_risque'
    eleve = 'haut_risque'




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
    updatedMap = input("Veuillez entrer une carte (avec l'extension .txt): ")
    hasBorne, graph = creerGraphe("centresLocaux.txt")    #il manque un controle de l'erreur dans creerGraphe (si on entre une mauvaise carte)
    lireGraphe(graph)                           #Ne fonctionne pas en ce moment
    global hasMap
    hasMap = 1
    print("Mise à jour de la carte!")                 
    menu()

def CheminPlusCourtSecuritaire():
    if hasMap == None:
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:
        transport = input("Veuillez entrer la catégorie de transport: ")
        origine = input("Veuillez entrer l'origine: ")
        destination = input("Veuillez entrer la destination: ")
        test1 = 'faible_risque'
        test2 = '1'
        test3 = '15'
        path = plusCourtChemin(test1, test2, test3)
        menu()

def ExtraireSousGraphe():
    if hasMap == None:
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:
        node = input("Veuillez entrer l'indice du sommet: ")
        vehicle = input("Veuillez entrer le type de véhicule (1: Ni-MH, 2: Li-ion): ")
        patient = input("Veuillez entrer le type de patient (1: faible risque, 2: moyen risque, 3: haut risque): ")
        #sousGraphe = extraireSousGraphe(node, vehicle, patient)
        #print(sousGraphe)
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