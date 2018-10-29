import collections
from enum import Enum

FIN_DE_LIGNE = "\n"
LIGNE_VIDE = "\n\n"
BATTERIE_PLEINE = 100

class Vehicule(Enum):
    NINH = 'NI-NH'
    LIion = 'LI-ion'

BorneRecharge, GrapheCLSCs = dict(), dict()

def creerGraphe(nomFichier):
    fichier = open(nomFichier,"r").read()
    
    bornesCLSC , arcs = fichier.split(LIGNE_VIDE)

    listeBornes = bornesCLSC.split(FIN_DE_LIGNE)
    listeArcs = arcs.split(FIN_DE_LIGNE)

    for ligne in listeBornes:
        numeroCLSC, aUneCharge = ligne.split(',')
        BorneRecharge[numeroCLSC] = aUneCharge

    for ligne in listeArcs:
        noeudA, noeudB, cout = ligne.split(',')
        
        if noeudA not in GrapheCLSCs:
            GrapheCLSCs[noeudA] = {}
        if noeudB not in GrapheCLSCs:
            GrapheCLSCs[noeudB] = {}
        
        GrapheCLSCs[noeudA][noeudB] = int(cout)
        GrapheCLSCs[noeudB][noeudA] = int(cout)

    return BorneRecharge,GrapheCLSCs

def lireGraphe(graphe):
    for node in graphe:
        print(node)
        print (graphe[node])
   
taux_decharge = {
    Vehicule.NINH : {
        'faible_risque' : (6/60),
        'moyen_risque' : (12/60),
        'haut_risque' : (48/60)
    },

    Vehicule.LIion : {
        'faible_risque' : (5/60),
        'moyen_risque' : (10/60),
        'haut_risque' : (30/60)
    }
}

#return [chemin, temps total, type vehicule, niveau batterie finale]
def plusCourtChemin(categorie_transport, origine, destination, type_vehicule=Vehicule.NINH):
    chemin, temps_chemin = algoDijkstra(GrapheCLSCs, origine, destination)
    
    temps_decharge_80 = 80/taux_decharge[type_vehicule][categorie_transport]
    niveau_batterie_finale = BATTERIE_PLEINE - taux_decharge[type_vehicule][categorie_transport]*temps_chemin

    chemin_trouve = False
    
    # Si la voiture se decharge avant d'arriver
    if(temps_chemin > temps_decharge_80):
        #On parcourt le chemin dans le sens inverse, et on trouve la premiere CLSC, ou on peut se recharger
        for clsc,temps_a_partir_origine in chemin[::-1]:
            if (temps_a_partir_origine < temps_decharge_80 and BorneRecharge[clsc]):
                print("On recharge a la borne : " + str(clsc))
                temps_ici_destination = temps_chemin - temps_a_partir_origine
                niveau_batterie_finale = BATTERIE_PLEINE - taux_decharge[type_vehicule][categorie_transport]*temps_ici_destination
                temps_chemin += 120
                chemin_trouve = True
                break
    else:
        chemin_trouve = True

    if(not chemin_trouve and type_vehicule is Vehicule.NINH):
        plusCourtChemin(categorie_transport,origine,destination,Vehicule.LIion)

    if(chemin_trouve):
        return[chemin, temps_chemin, type_vehicule, niveau_batterie_finale]
    else:
        print("Impossible")
        return None

# returns a tuple (set [node : time from origin], total time)
def algoDijkstra(graphe, origine, destination):
    # le tuple est (previous_node, time_from_origin)
    plus_courts_chemins = {origine : (None, 0)}
    
    noeud_courant = origine
    noeuds_visites = set()

    while noeud_courant != destination:
        noeuds_visites.add(noeud_courant)

        temps_origine_a_courant = plus_courts_chemins[noeud_courant][1]

        #on parcourt tous les voisins du noeud courant
        for voisin in graphe[noeud_courant]:
            temps_origine_a_voisin = graphe[noeud_courant][voisin] + temps_origine_a_courant

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
  
  def extraireSousGraphe(transport_category, origin, type_vehicule=Vehicule.NINH):
    
    graphe = GrapheCLSCs
    longest_paths = {origin : (None, 0)}
    current_node = origin
    visited = set()

    time_to_consume_80 = 80/battery_cost[type_vehicule][transport_category]

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
            breaks

    path = []

    while current_node is not None:
        path.append((current_node, longest_paths[current_node][1]))
        next_node = longest_paths[current_node][0]
        current_node = next_node

    path = path[::-1]

    return [path, current_time]