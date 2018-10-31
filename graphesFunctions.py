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

#Vérifie si le fichierexiste
#Retourne un Boolean
def fichierExiste(nomFichier):
    if(os.path.isfile(nomFichier)):
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

# Si le GrapheCLSCs existe, il l'imprime, sinon imprime Erreur
def lireGraphe():
    for node in GrapheCLSCs:
        print(node)
        print (GrapheCLSCs[node])

# Parametres : Risque.type, le noeud d'origine et la destinatinons (en string)
# Retourne [[chemin], temps total, Vehicule.type, niveau batterie finale]
def plusCourtChemin(risque_transport, origine, destination, type_vehicule = Vehicule.NI_MH):

    chemin, temps_chemin = algoDijkstra(origine, destination)

    temps_decharge_80 = 80/taux_decharge[type_vehicule][risque_transport]
    niveau_batterie_finale = BATTERIE_PLEINE - taux_decharge[type_vehicule][risque_transport]*temps_chemin

    chemin_trouve = False
    
    # Si la voiture se decharge avant d'arriver
    if(temps_chemin > temps_decharge_80):
        #On parcourt le chemin dans le sens inverse, et on trouve la premiere CLSC, ou on peut se recharger
        for clsc,temps_a_partir_origine in chemin[::-1]:
            if (temps_a_partir_origine < temps_decharge_80 and BorneRecharge[clsc]):
                print("On recharge a la borne : " + str(clsc))
                temps_ici_destination = temps_chemin - temps_a_partir_origine
                niveau_batterie_finale = BATTERIE_PLEINE - taux_decharge[type_vehicule][risque_transport]*temps_ici_destination
                temps_chemin += TEMPS_RECHARGE
                chemin_trouve = True
                break
    else:
        chemin_trouve = True

    # Si la voiture se decharge en chemin, et qu'il n'y a pas de Bornes,
    # On calcule le plus court chemin de origine jusqua toutes les bornes de recharge ET
    # le plus cours chemin de toutes les bornes de recharge jusqu'a destination
    if(not chemin_trouve):
        trouverPlusCourtCheminAvecBorneRecharge(temps_decharge_80, origine, destination)
    # doit retourner qqchose ici ----

    # Si on ne trouve toujours pas de chemin possible avec le vehicule NI-MH, on essaye avec
    # un vehicule LI-ion
    if(not chemin_trouve and type_vehicule is Vehicule.NINH):
        plusCourtChemin(risque_transport,origine,destination,Vehicule.LIion)

    if(chemin_trouve):
        return[chemin, temps_chemin, type_vehicule, niveau_batterie_finale]
    else:
        return None

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

# Retourne un tupe (set [noeud : temps a partir d'origine], temps total)
def trouverPlusCourtCheminAvecBorneRecharge(temps_decharge_80, origine, destination):
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
    # Un peu le bordel icite...

    for cheminTotal in cheminsOrigineDestinationAvecBorne:
        tempsOrigineBorne = cheminTotal[0][1]
        cheminOrigineBorne = cheminTotal[0][0]
        tempsBorneDestination = cheminTotal[1][1]
        cheminBorneDestination = cheminTotal[1][0]
        tempsTotal = tempsOrigineBorne + tempsBorneDestination + TEMPS_RECHARGE
        cheminTotal = cheminOrigineBorne + cheminBorneDestination
        print(cheminTotal)
        
        if (tempsTotal < tempsMinimal):
            tempsMinimal = tempsTotal
        

    print(cheminsOrigineDestinationAvecBorne)


# Parametres : Risque.type, noeud origine et destination (en string), et Vehicule.Type
# Retourne [[chemin], temps total]
def extraireSousGraphe(transport_category, origin, type_vehicule):

    graphe = GrapheCLSCs
    longest_paths = {origin : (None, 0)}
    current_node = origin
    visited = set()

    time_to_consume_80 = 80/taux_decharge[type_vehicule][transport_category]

    while(longest_paths[current_node][1] < time_to_consume_80):
        visited.add(current_node)

        current_time = longest_paths[current_node][1]

        #on parcourt tous les voisins du noeud courant
        for neighbour in graphe[current_node]:
            time_from_origin_to_neighbour = graphe[current_node][neighbour] + current_time

            if neighbour not in longest_paths:
                longest_paths[neighbour] = (current_node, time_from_origin_to_neighbour)
            else:
                current_longest_time = longest_paths[neighbour][1]
                if time_from_origin_to_neighbour > current_longest_time:
                    if longest_paths[neighbour][0] not in visited:
                        if longest_paths[neighbour][0] != None:
                            longest_paths[neighbour] = (current_node, time_from_origin_to_neighbour)

        next_destinations = {node : longest_paths[node] for node in longest_paths if node not in visited }
        if(next_destinations):
            current_node = max(next_destinations, key=lambda k:next_destinations[k][1])
        else:
            break

    path = []

    while current_node is not None:
        path.append((current_node, longest_paths[current_node][1]))
        next_node = longest_paths[current_node][0]
        current_node = next_node

    path = path[::-1]

    return [path, current_time]