import collections
from enum import Enum

END_OF_LINE = "\n"
EMPTY_LINE = "\n\n"
BATTERIE_PLEINE = 100

class Vehicule(Enum):
    NINH = 'NI-NH'
    LIion = 'LI-ion'

BorneRecharge, GrapheCLSCs = dict(), dict()

def creerGraphe(fileName):
    file = open(fileName,"r").read()
    
    bornesCLSC,arcs = file.split(EMPTY_LINE)

    listBornes = bornesCLSC.split(END_OF_LINE)
    listArcs = arcs.split(END_OF_LINE)

    for line in listBornes:
        numero, hasCharge = line.split(',')
        BorneRecharge[numero] = hasCharge

    for line in listArcs:
        nodeA, nodeB, cost = line.split(',')
        
        if nodeA not in GrapheCLSCs:
            GrapheCLSCs[nodeA] = {}
        if nodeB not in GrapheCLSCs:
            GrapheCLSCs[nodeB] = {}
        
        GrapheCLSCs[nodeA][nodeB] = int(cost)
        GrapheCLSCs[nodeB][nodeA] = int(cost)

    return BorneRecharge,GrapheCLSCs

def lireGraphe(graphe):
    for node in graphe:
        print(node)
        print (graphe[node])
   
battery_cost = {
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

def plusCourtChemin(transport_category, origine, destination):
    path, path_time = dijkstraPath(GrapheCLSCs, origine, destination)
    
    time_to_consume_80_NINH = 80/battery_cost[Vehicule.NINH][transport_category]
    battery_finale = BATTERIE_PLEINE - battery_cost[Vehicule.NINH][transport_category]*path_time

    print("time_to_consume_80_NINH = " + str(time_to_consume_80_NINH))

    if(path_time > time_to_consume_80_NINH):
        #sinon on va parcourir le chmin a lenvers a partir du moment ou la batterie est en dessous de 20 pour trouver la premiere borne de recharge
        for clsc,time_to_node in path[::-1]:
            if (time_to_node < time_to_consume_80_NINH and BorneRecharge[clsc]):
                print("On recharge a la borne : " + str(clsc))
                time_recharge_destination = path_time - time_to_node
                battery_finale = BATTERIE_PLEINE - battery_cost[Vehicule.NINH][transport_category]*time_recharge_destination
                path_time += 120
                break
    
    return[path, path_time, Vehicule.NINH, battery_finale]



# returns a tuple (set of nodes to go through, total time)
def dijkstraPath(graphe, origin, destination):
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
