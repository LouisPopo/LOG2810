def MoveNodeToVisited(key, unvisited, visited):
    visited.add(key)
    del unvisited[key]

def PlusCourtCheminTest(graphe, typeParcours = None, origine = '1', destination = '8'):
    visited, parcours = set(), list()
    unvisited = {node: float('inf') for node in graphe} #mets la distance a 'Infini' pour tous les points

    unvisited[origine] =  0               #mets la distance a '0' pour le point de depart
    MoveNodeToVisited(origine, unvisited, visited)
    print("UNVISITED AU DEBUT")
    print (unvisited)
    print (visited)
    return 0