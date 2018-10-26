def MoveCurrentNodeToVisited(key, unvisited, visited):
    visited.add(key)
    del unvisited[key]

def SetNeighborNodes(unvisited, visited, graphe):
    for node in visited
        for neighbor_node in graphe[node]
            if graphe[node][neighbor_node] < unvisited[graphe[node][neighbor_node]]

def FindNextNode(unvisited, visited, graphe):
   





def PlusCourtCheminTest(graphe, typeParcours = None, origine = '1', destination = '8'):
    
    visited, parcours = set(), list()
    
    unvisited = {node: float('inf') for node in graphe} #mets la distance a 'Infini' pour tous les points
    unvisited[origine] =  0                              #mets la distance a '0' pour le point de depart
    MoveCurrentNodeToVisited(origine, unvisited, visited)

    print("UNVISITED AU DEBUT")
    print (unvisited)
    print (visited)
    return 0