import collections
from dictionnaires import *
import os.path

FIN_DE_LIGNE = "\n"
LIGNE_VIDE = "\n\n"
BATTERIE_PLEINE = 100
TEMPS_RECHARGE = 120

# Dictionnaire avec les CLSCs qui ont des bornes de recharge et le Graphe de toutes les CLSCs
BorneRecharge, GrapheCLSCs = dict(), dict()

def fichierExiste(nomFichier):
    return os.path.isfile(nomFichier)

#Verifie si le noeud existe
def noeudExiste(noeud):
    if noeud in GrapheCLSCs:
        return True
    return False

# Verifie si le graphe Existe
# Retourne un Boolean
def grapheExiste():
    if (GrapheCLSCs):
        return True
    return False

# Parametre : chemin vers le fichier
# Si le chemin est valide, il cree un Graphe, sinon imprime Erreur
# Ne retourne Rien
def creerGraphe( nomFichier):
    
    BorneRecharge.clear()
    GrapheCLSCs.clear()
    
    fichier = open(nomFichier,"r").read()

    bornesCLSC , arcs = fichier.split(LIGNE_VIDE)

    listeBornes = bornesCLSC.split(FIN_DE_LIGNE)
    listeArcs = arcs.split(FIN_DE_LIGNE)

    for ligne in listeBornes:
        numeroCLSC, aUneCharge = ligne.split(',')
        BorneRecharge[numeroCLSC] = (aUneCharge == '1')

    for ligne in listeArcs:
        noeudA, noeudB, cout = ligne.split(',')
        
        if noeudA not in GrapheCLSCs:
            GrapheCLSCs[noeudA] = {}
        if noeudB not in GrapheCLSCs:
            GrapheCLSCs[noeudB] = {}
        
        GrapheCLSCs[noeudA][noeudB] = int(cout)
        GrapheCLSCs[noeudB][noeudA] = int(cout)

# Si le GrapheCLSCs existe, il l'imprime
def lireGraphe():
    print("Noeud : { Voisin_1 : duree, Voisin_2 : duree, ... }")
    for node in GrapheCLSCs:
        print (str(node) + " : " + str(GrapheCLSCs[node]))

# Parametres : Risque.type, le noeud d'origine et la destinatinons (en string)
# Retourne un dictionnaire : (Chemin : [liste], TempsTotal : int, Batterie : int, Vehicule : Vehicule)
# OU None si impossible
def plusCourtChemin(risque_transport, origine, destination, type_vehicule = Vehicule.NI_MH):

    chemin, temps_chemin = algoDijkstra(origine, destination)

    tauxDecharge = dictTauxDecharge[type_vehicule][risque_transport]

    temps_decharge_80 = 80/tauxDecharge
    niveau_batterie_finale = BATTERIE_PLEINE - tauxDecharge*temps_chemin

    chemin_trouve = False
    
    resultat = None

    # Si la voiture se decharge avant d'arriver
    if(temps_chemin > temps_decharge_80):
        #On parcourt le chemin dans le sens inverse, et on trouve la premiere CLSC, ou on peut se recharger
        for clsc,temps_a_partir_origine in chemin[::-1]:
            if (temps_a_partir_origine < temps_decharge_80 and BorneRecharge[clsc]):
                print("On recharge a la borne : " + str(clsc))
                temps_ici_destination = temps_chemin - temps_a_partir_origine
                niveau_batterie_finale = BATTERIE_PLEINE - tauxDecharge*temps_ici_destination
                temps_chemin += TEMPS_RECHARGE
                chemin_trouve = True
                break
    else:
        chemin_trouve = True
    
    resultat = {
        'Chemin' : creerListeChemin(chemin),
        'TempsTotal' : temps_chemin,
        'Batterie' : niveau_batterie_finale,
        'Vehicule' : type_vehicule
    }

    # Si la voiture se decharge en chemin, et qu'il n'y a pas de Bornes,
    # On calcule le plus court chemin de origine jusqua toutes les bornes de recharge ET
    # le plus cours chemin de toutes les bornes de recharge jusqu'a destination
    if(not chemin_trouve):
        print('Chemin le plus court ne contient pas de bornes de recharge')
        resultat = trouverPlusCourtCheminAvecBorneRecharge(temps_decharge_80, origine, destination, tauxDecharge)
        resultat['Vehicule'] = type_vehicule
    # doit retourner qqchose ici ----

    # Si on ne trouve toujours pas de chemin possible avec le vehicule NI-MH, on essaye avec
    # un vehicule LI-ion
    if(resultat == None and type_vehicule == Vehicule.NI_MH):
        plusCourtChemin(risque_transport,origine,destination,Vehicule.LI_ion)

    return resultat

# Retourne un tuple (set [noeud : temps a partir d'origine], temps total)
def algoDijkstra(origine, destination):
    # le tuple est (previous_node, time_from_origin)
    plus_courts_chemins = {origine : (None, 0)}
    
    noeud_courant = origine
    noeuds_visites = set()

    while noeud_courant != destination:
        noeuds_visites.add(noeud_courant)

        temps_origine_a_courant = plus_courts_chemins[noeud_courant][1]

        #on parcourt tous les voisins du noeud courant
        for voisin in GrapheCLSCs[noeud_courant]:
            temps_origine_a_voisin = GrapheCLSCs[noeud_courant][voisin] + temps_origine_a_courant

            if voisin not in plus_courts_chemins:
                plus_courts_chemins[voisin] = (noeud_courant, temps_origine_a_voisin)
            else:
                temps_minimal_actuel = plus_courts_chemins[voisin][1]
                if temps_origine_a_voisin < temps_minimal_actuel:
                    plus_courts_chemins[voisin] = (noeud_courant,temps_origine_a_voisin)
        
        prochains_noeuds = {node : plus_courts_chemins[node] for node in plus_courts_chemins if node not in noeuds_visites }

        noeud_courant = min(prochains_noeuds, key=lambda k:prochains_noeuds[k][1])


    chemin=[]
    #noeud_courant = destination
    #chemin = set tuples(node, time from origin)
    # On parcourt le dictionnaire 'plus_courts_chemins' : en partant de 'destination' et en allant ensuite au noeud present dans le tuple
    while noeud_courant is not None:
        chemin.append((noeud_courant, plus_courts_chemins[noeud_courant][1]))
        prochain_noeud = plus_courts_chemins[noeud_courant][0]
        noeud_courant = prochain_noeud

    #on inverse l'ordre du tableau
    chemin = chemin[::-1]
    return (chemin, plus_courts_chemins[destination][1])

# Retourne un dictionnaire (Chemin : [liste], TempsTotal : int, Batterie : int)
# OU None si impossible
def trouverPlusCourtCheminAvecBorneRecharge(temps_decharge_80, origine, destination, tauxDecharge):
    # On prend toutes les CLSCs qui ont des bornes de recharge
    idsCLSCsAvecBorne = list(filter(BorneRecharge.get, BorneRecharge))
     
    cheminsOrigineBornes = []

    for clsc in idsCLSCsAvecBorne:
        if clsc != origine:
            chemin = algoDijkstra(origine,clsc)
            if(chemin[1] < temps_decharge_80):
                cheminsOrigineBornes.append(chemin)


    cheminsOrigineDestinationAvecBorne = []

    for cheminJusquaBorneEtTemps in cheminsOrigineBornes:
        idBorne = cheminJusquaBorneEtTemps[0][-1][0]    # On prend le premier element du tuple, qui est une liste, 
                                                        # de laquelle on prend le dernier element, qui est un autre tuple 
                                                        # (noeud, temps a partir d'origine ), duquel on prend le noeud seulement

        borneJusquaDestination = algoDijkstra(idBorne,destination)
        if(borneJusquaDestination[1] < temps_decharge_80):
            cheminsOrigineDestinationAvecBorne.append((cheminJusquaBorneEtTemps,borneJusquaDestination))

    
    tempsMinimal = float('inf')

    # A ce moment, cheminsOrigineDestinationAvecBorne est une liste de tuple

    resultat = None

    for cheminTotal in cheminsOrigineDestinationAvecBorne:
        tempsOrigineBorne = cheminTotal[0][1]
        tempsBorneDestination = cheminTotal[1][1]
        tempsTotal = tempsOrigineBorne + tempsBorneDestination + TEMPS_RECHARGE

        if tempsBorneDestination < temps_decharge_80 and tempsTotal < tempsMinimal:
            tempsMinimal = tempsTotal
            cheminOrigineBorne = creerListeChemin(cheminTotal[0][0])[:-1]
            cheminBorneDestination = creerListeChemin(cheminTotal[1][0])
            cheminTotal = cheminOrigineBorne + cheminBorneDestination
            niveauBatterie = BATTERIE_PLEINE - tempsBorneDestination*tauxDecharge
            resultat = {
                'Chemin' : cheminTotal,
                'TempsTotal' : tempsTotal,
                'Batterie' : niveauBatterie
            }
        

    return(resultat)

# Transfomre une liste de Tuples(CLSC, tempsAPartirOrignie) en liste de [CLSCs]
def creerListeChemin(listeTupleCheminTemps):
    resultat = []
    for noeudTemps in listeTupleCheminTemps:
        resultat.append(noeudTemps[0])
    return resultat




# Parametres : Risque.type, noeud origine et destination (en string), et Vehicule.Type
# Retourne [[chemin], temps total]
def extraireSousGraphe(categorie_transport, origine, type_vehicule=Vehicule.NINH):
    graphe = GrapheCLSCs
    noeud_courant = origine
    noeud_precedent = None
    temps_decharge_80 = 80/taux_decharge[type_vehicule][categorie_transport]

    chemins_possibles = trouverCheminsPossibles(noeud_precedent, noeud_courant, temps_decharge_80, graphe, 0)

    plusLongChemin = max(chemins_possibles, key=lambda k:chemins_possibles[k][k][1])
    return [chemins_possibles[plusLongChemin][0], chemins_possibles[plusLongChemin][1]]


def trouverCheminsPossibles(noeud_precedent, noeud_courant, temps_decharge_80, graphe, chemin_actuel):
    
    for voisin in graphe[noeud_courant][voisin]:
        chemins_possibles = {} #{0 : [[1,2,3,4], temps], 1: [[5,6,7], temps2]}
        voisins = []
        #Met tous les voisins dans voisins[] et enlever les noeuds deja visites
        
        for voisin in graphe[noeud_courant][voisin]:
            voisins.append(voisin)
        for voisin in voisins:
            if voisin in chemins_possibles[chemin_actuel][0]:
                voisins.remove(voisin)
        
        if voisins:
            for voisin in voisins:
                if (chemins_possibles[chemin_actuel][1] <= temps_decharge_80):
                    chemins_possibles[chemin_actuel][0].append(noeud_courant)
                    chemins_possibles[chemin_actuel][1] += graphe[noeud_precedent][noeud_courant]
                    noeud_precedent = noeud_courant
                    noeud_courant = voisin
        else:
            chemin_actuel += 1
    
    return chemins_possibles



    # graphe = GrapheCLSCs
    # plus_longs_chemins = {origine : (None, 0)}
    # noeud_courant = origine
    # noeuds_visites = set()

    # temps_decharge_80 = 80/taux_decharge[type_vehicule][categorie_transport]

    # while(plus_longs_chemins[noeud_courant][1] < temps_decharge_80):
    #     noeuds_visites.add(noeud_courant)

    #     temps_actuel = plus_longs_chemins[noeud_courant][1]

    #     #on parcourt tous les voisins du noeud courant
    #     for voisin in graphe[noeud_courant]:
    #         temps_origine_a_voisin = graphe[noeud_courant][voisin] + temps_actuel

    #         if voisin not in plus_longs_chemins:
    #             plus_longs_chemins[voisin] = (noeud_courant, temps_origine_a_voisin)
    #         else:
    #             temps_maximal_actuel = plus_longs_chemins[voisin][1]
    #             if temps_origine_a_voisin > temps_maximal_actuel:
    #                 if plus_longs_chemins[voisin][0] not in noeuds_visites:
    #                     if plus_longs_chemins[voisin][0] != None:
    #                         plus_longs_chemins[voisin] = (noeud_courant, temps_origine_a_voisin)

    #     prochains_noeuds = {noeud : plus_longs_chemins[noeud] for noeud in plus_longs_chemins if noeud not in noeuds_visites }
    #     if(prochains_noeuds):
    #         noeud_courant = max(prochains_noeuds, key=lambda k:prochains_noeuds[k][1])
    #     else:
    #         break

    # chemin = []

    # while noeud_courant is not None:
    #     chemin.append((noeud_courant, plus_longs_chemins[noeud_courant][1]))
    #     prochain_noeud = plus_longs_chemins[noeud_courant][0]
    #     noeud_courant = prochain_noeud

    # chemin = chemin[::-1]

    # return [chemin, temps_actuel]

    