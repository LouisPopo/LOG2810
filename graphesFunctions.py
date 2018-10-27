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
                time_recharge_destination = temps_chemin - temps_a_partir_origine
                niveau_batterie_finale = BATTERIE_PLEINE - taux_decharge[type_vehicule][categorie_transport]*time_recharge_destination
                temps_chemin += 120
                chemin_trouve = True
                break

    if(not chemin_trouve and type_vehicule is Vehicule.NINH):
        plusCourtChemin(categorie_transport,origine,destination,Vehicule.LIion)

    if(chemin_trouve):
        return[chemin, temps_chemin, type_vehicule, niveau_batterie_finale]
    else:
        print("Impossible")
        return None



# returns a tuple (set [node : time from origin], total time)
def algoDijkstra(graphe, origin, destination):
    # le tuple est (previous_node, time_from_origin)
    shortest_paths = {origin : (None, 0)}
    
    current_node = origin
    visited = set()

    while current_node != destination:
        visited.add(current_node)

        current_time = shortest_paths[current_node][1]

        #on parcourt tous les voisins du noeud courant
        for neighbour in graphe[current_node]:
            time_from_origin_to_neighbour = graphe[current_node][neighbour] + current_time

            if neighbour not in shortest_paths:
                shortest_paths[neighbour] = (current_node, time_from_origin_to_neighbour)
            else:
                current_shortest_time = shortest_paths[neighbour][1]
                if time_from_origin_to_neighbour < current_shortest_time:
                    shortest_paths[neighbour] = (current_node,time_from_origin_to_neighbour)
        
        next_destinations = {node : shortest_paths[node] for node in shortest_paths if node not in visited }

        current_node = min(next_destinations, key=lambda k:next_destinations[k][1])


    path=[]
    #current_node = destination
    #path = set tuples(node, time from origin)
    # On parcourt le dictionnaire 'shortest_paths' : en partant de 'destination' et en allant ensuite au noeud present dans le tuple
    while current_node is not None:
        path.append((current_node, shortest_paths[current_node][1]))
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    #on inverse l'ordre du tableau
    path = path[::-1]
    return (path, shortest_paths[destination][1])
