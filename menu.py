from graphesFunctions import *
from enum import Enum
from dictionnaires import *

#TODO: print de nabs

#Affichage des choix
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

#Option a: mise a jour du graphe
def MiseAJour():
    grapheMisAJour = input("Veuillez entrer une carte (avec l'extension .txt): ")

    #Controle de l'erreur: On cree le graphe seulement si le fichier existe
    if fichierExiste(grapheMisAJour):
        creerGraphe(grapheMisAJour)
    else:
        print ("Le nom de fichier n'existe pas")
    
    #La lecture n'est fait que si le graphe existe
    if grapheExiste():   
        lireGraphe()                       
        print("Mise à jour de la carte!")
    else:
        print ("Le graphe n'existe pas")

    menu()

#Option b: chemin le plus court securitaire
def CheminPlusCourtSecuritaire():

    #Controle de l'existance du graphe. On doit creer un graphe avant de pouvoir 
    #trouver le chemin le plus court securitaire
    if not grapheExiste():
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:

        #Initialisation
        transport = 0
        origine = destination = -1

        #On controle l'erreur pour chaque entree de l'utilisateur. Si l'entree n'est
        #pas possible, on renvoie un message d'erreur et on reaffiche le message
        #d'entree
        while transport not in dictRisque: 
            transport = input("Veuillez entrer la catégorie de transport (1: faible risque, 2: moyen risque, 3: haut risque): ")
            if transport not in dictRisque:    
                print("Ceci n'est pas un option!")
        
        while not noeudExiste(origine):
            origine = input("Veuillez entrer l'origine: ")
            if not noeudExiste(origine):    
                print("Ce noeud n'existe pas!")

        while not noeudExiste(destination):
            destination = input("Veuillez entrer la destination: ") 
            if not noeudExiste(destination):    
                print("Ce noeud n'existe pas!")

        #On envoie les parametres de l'utilisateur a la fonction
        chemin = plusCourtChemin(dictRisque[transport], origine, destination)

        #Si le chemin existe, on affiche chaque parametre du dit chemin. Sinon, on
        #affiche que le chemin est impossible et on retourne au menu
        if chemin is not None:
            print("\nChemin: " + str(chemin['Chemin'])) 
            print("Temps: " + str(chemin['TempsTotal']))
            print("Type de véhicule: " + str(chemin['Vehicule']))
            print("Niveau de batterie final: " + str(chemin['Batterie']))   
        else:
            print("Ce chemin n'est pas possible!")
        menu()

#Option c: extraire un sous graphe
def ExtraireSousGraphe():

    #Controle de l'existance du graphe. On doit creer un graphe avant de pouvoir 
    #extraire un sous graphe
    if not grapheExiste():
        print ("Veuillez d'abord mettre une carte à jour!")
        menu()
    else:

        #Initialisation
        vehicule = patient = 0
        noeud = -1

        #On controle l'erreur pour chaque entree de l'utilisateur. Si l'entree n'est
        #pas possible, on renvoie un message d'erreur et on reaffiche le message
        #d'entree
        while not noeudExiste(noeud):
            noeud = input("Veuillez entrer l'indice du sommet: ")
            if not noeudExiste(noeud):
                print("Ce noeud n'existe pas!")

        while vehicule not in dictVehicule:   
            vehicule = input("Veuillez entrer le type de véhicule (1: Ni-MH, 2: Li-ion): ")
            if vehicule not in dictVehicule:    
                print("Ceci n'est pas un option!")

        while patient not in dictRisque:
            patient = input("Veuillez entrer le type de patient (1: faible risque, 2: moyen risque, 3: haut risque): ")
            if patient not in dictRisque:    
                print("Ceci n'est pas un option!")
        
        #On envoie les parametres de l'utilisateur a la fonction
        sousGraphe = extraireSousGraphe(dictRisque[patient], noeud, dictVehicule[vehicule])

        #Si le chemin a extraire existe, on affiche chaque parametre du dit chemin. 
        #Sinon, on affiche que le chemin voulu est impossible et on retourne au menu
        if sousGraphe is not None:
            print("\nChemin: " + str(sousGraphe))  
        else:
            print("Ce sous-graphe n'existe pas!")
        menu()

#Option d: quitter
#On affiche la fin du programme et on retourn 0
def Quitter():
    print("Fin du programme")
    return 0

#Option menu
#Il s'agit de la fonction appellee a la base par le main
#Elle permet la centralisation des autres fonctions
def menu():

    #Dictionnaire des options possibles
    options = { 'a' : MiseAJour,
                'b' : CheminPlusCourtSecuritaire,
                'c' : ExtraireSousGraphe,
                'd' : Quitter,
    }

    #On affiche le menu et on demande a l'utilisateur l'option qu'il veut choisir
    Affichage()
    choix = input("Veuillez entrer un option (a, b, c ou d): ")

    #Si le choix existe dans le dictionnaire options, on renvoie l'utilisateur a 
    #l'option voulue. Sinon, on affiche un message d'erreur et on revient au menu
    if choix in options:
        print("Vous avez entré: " + choix)
        options[choix]()
    else:
        print("Cette option n'existe pas. Veuillez choisir l'une des option possible: ")
        menu()