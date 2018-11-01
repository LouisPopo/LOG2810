from graphesFunctions import creerGraphe, plusCourtChemin, lireGraphe, grapheExiste, extraireSousGraphe, fichierExiste
from enum import Enum
from dictionnaires import *

#TODO: manage les tests

dictVehicule = {'1' : Vehicule.NI_MH,
                '2' : Vehicule.LI_ion}

dictRisque = {'1' : Risque.faible,
              '2' : Risque.moyen,
              '3' : Risque.haut}

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
    updatedMap = input("Veuillez entrer une carte (avec l'extension .txt): ") #TODO

    if fichierExiste("centresLocaux.txt"):
        creerGraphe("centresLocaux.txt")
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

        while transport not in dictRisque: 
            transport = input("Veuillez entrer la catégorie de transport (1: faible risque, 2: moyen risque, 3: haut risque): ")
            if transport not in dictRisque:    
                print("Ceci n'est pas un option!")

        origine = input("Veuillez entrer l'origine: ")                 #gestion de lerreur sur un noeud non-existant
        destination = input("Veuillez entrer la destination: ")        #gestion de lerreur sur un noeud non-existant

        path = plusCourtChemin(dictRisque[transport], origine, destination)
        if path is not None:
            print("Chemin: " + path[0]) #TODO
            print("Temps: " + path[1])
            print("Type de véhicule: " + path[2])
            print("Niveau de batterie final: " + path[3])   
        else:
            print("Ce chemin n'est pas possible!")      #print plus complexe a faire
        menu()

def ExtraireSousGraphe():
    if not grapheExiste():
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:
        vehicle = patient = 0
        node = input("Veuillez entrer l'indice du sommet: ")     #gestion de lerreur sur un noeud non-existant

        while vehicle not in dictVehicule:   
            vehicle = input("Veuillez entrer le type de véhicule (1: Ni-MH, 2: Li-ion): ")
            if vehicle not in dictVehicule:    
                print("Ceci n'est pas un option!")

        while patient not in dictRisque:
            patient = input("Veuillez entrer le type de patient (1: faible risque, 2: moyen risque, 3: haut risque): ")
            if patient not in dictRisque:    
                print("Ceci n'est pas un option!")

        sousGraphe = extraireSousGraphe(dictRisque[patient], node, dictVehicule[vehicle])
        if sousGraphe is not None:
            print("Chemin: ")
            for m in sousGraphe[0]:
                print(sousGraphe[0][m])             #??? #TODO
            #print("Temps: " + sousGraphe[1])        #transformer en str
        else:
            print("Ce sous-graphe n'existe pas!")
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