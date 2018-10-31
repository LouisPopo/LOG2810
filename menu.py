from graphesFunctions import creerGraphe, plusCourtChemin, lireGraphe, grapheExiste, extraireSousGraphe, fichierExiste
from enum import Enum
from dictionnaires import *

#TODO: manage les tests



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

    if fichierExiste(updatedMap):
        creerGraphe(updatedMap)
    else:
        print ("Le nom de fichier n'existe pas")
    
    if grapheExiste():   
        lireGraphe()                       
        print("Mise à jour de la carte!")
    else:
        print ("Le graphe n'existe pas")

    menu()

def CheminPlusCourtSecuritaire():
    if not grapheExiste():
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:
        transport = 0

        while transport not in Risque.__members__: 
            transport = input("Veuillez entrer la catégorie de transport (faible: faible risque, moyen: moyen risque, haut: haut risque): ")
            if transport not in Risque.__members__:    
                print("Ceci n'est pas un option!")

        origine = input("Veuillez entrer l'origine: ")                 #gestion de lerreur sur un noeud non-existant
        destination = input("Veuillez entrer la destination: ")        #gestion de lerreur sur un noeud non-existant

        path = plusCourtChemin(dictRisque[transport], origine, destination)
        print(path)         #print plus complexe a faire
        menu()

def ExtraireSousGraphe():
    if not grapheExiste():
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:
        vehicle = patient = 0
        node = input("Veuillez entrer l'indice du sommet: ")     #gestion de lerreur sur un noeud non-existant

        while vehicle not in Vehicule.__members__:   
            vehicle = input("Veuillez entrer le type de véhicule (1: Ni-MH, 2: Li-ion): ")
            if vehicle not in Vehicule.__members__:    
                print("Ceci n'est pas un option!")

        while patient not in Risque.__members__:
            patient = input("Veuillez entrer le type de patient (1: faible risque, 2: moyen risque, 3: haut risque): ")
            if patient not in Risque.__members__:    
                print("Ceci n'est pas un option!")

        sousGraphe = extraireSousGraphe(dictRisque[patient], node, dictVehicule[vehicle])
        print(sousGraphe)        #print plus complexe a faire
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