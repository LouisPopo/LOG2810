from graphesFunctions import creerGraphe, plusCourtChemin, lireGraphe, verifierExistenceGraphe, extraireSousGraphe
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
    creerGraphe(updatedMap)   
    lireGraphe()                       
    #print("Mise à jour de la carte!")   #dans son fichier              
    menu()

def CheminPlusCourtSecuritaire():
    if not verifierExistenceGraphe():
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
        test1 = Risque.haut
        test2 = '1'
        test3 = '15'
        path = plusCourtChemin(test1, test2, test3)
        print(path)
        menu()

def ExtraireSousGraphe():
    if not verifierExistenceGraphe():
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:
        vehicle = patient = 0
        node = input("Veuillez entrer l'indice du sommet: ")     #gestion de lerreur sur un noeud non-existant

        while vehicle not in Vehicule.__members__:   
            vehicle = input("Veuillez entrer le type de véhicule (Ni-MH ou Li-ion): ")
            if vehicle not in Vehicule.__members__:    
                print("Ceci n'est pas un option!")

        while patient not in Risque.__members__:
            patient = input("Veuillez entrer le type de patient (faible: faible risque, moyen: moyen risque, haut: haut risque): ")
            if patient not in Risque.__members__:    
                print("Ceci n'est pas un option!")

        test4 = Risque.haut
        test5 = '1'
        test6 = Vehicule.LI_ion

        sousGraphe = extraireSousGraphe(test4, test5, test6)
        print(sousGraphe)
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