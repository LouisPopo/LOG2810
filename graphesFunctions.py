import collections

END_OF_LINE = "\n"
EMPTY_LINE = "\n\n"

CLSCs, GrapheCLSCs = dict(), dict()

def creerGraphe(fileName):
    file = open(fileName,"r").read()
    
    bornesCLSC,arcs = file.split(EMPTY_LINE)

    listBornes = bornesCLSC.split(END_OF_LINE)
    listArcs = arcs.split(END_OF_LINE)

    for line in listBornes:
        numero, hasCharge = line.split(',')
        CLSCs[numero] = hasCharge

    for line in listArcs:
        nodeA, nodeB, cost = line.split(',')
        
        if nodeA not in GrapheCLSCs:
            GrapheCLSCs[nodeA] = {}
        if nodeB not in GrapheCLSCs:
            GrapheCLSCs[nodeB] = {}
        
        GrapheCLSCs[nodeA][nodeB] = int(cost)
        GrapheCLSCs[nodeB][nodeA] = int(cost)

    return CLSCs,GrapheCLSCs

def lireGraphe(graphe):
    for node in graphe:
        print(node)
        print (graphe[node])

def plusCourtChemin(graphe, typeParcours = None, origine = 'A', destination = 'E'):

    print(graphe)
    
    visited, parcours = list(), list()
    unvisited = {node: float('inf') for node in graphe} #mets la distance a 'Infini' pour tous les points
    dist = dict()
    dist[origine] = 0
    

    current = origine
    currentTime = 0
    unvisited[origine] = currentTime                                             #mets la distance a '0' pour le point de depart


    while unvisited:
        print("--Unvisited--")
        print(unvisited)
        print("Visited")
        print(visited)
        # 3. Select the unvisited node with the smallest distance, 
        # it's origin the first time.
        current = min(unvisited, key= lambda cost: unvisited.get(cost))  

        # 4. Find unvisited neighbors for the current node 
        # and calculate their distances through the current node.

        for neighbour in graphe[current]:
            if neighbour in unvisited:
                newCost = graphe[current][neighbour] + currentTime

                # Compare the newly calculated distance to the assigned 
                # and save the smaller one.

                if newCost < unvisited[neighbour]:
                    unvisited[neighbour] = newCost

        # 5. Mark the current node as visited 
        # and remove it from the unvisited set.

        visited.append(current)
        del unvisited[current] 

    print(visited)
    print(dist)
        
        
    '''
        c

                                    #Ajoute le noeud trouve au CLSC visites
                                    #L'enleve des CLSCS non visites
        for neighbor in GrapheCLSCs[current]:                           #Cherche parmis les voisins de ce noeud
            if neighbor not in visited:                                             #Si on a pas deja visite le voisin
                if GrapheCLSCs[current][neighbor] < unvisited[neighbor]:        #Si la distance entre le noeud et son voisin est plus petite que celle qui avait avant  
                    unvisited[neighbor] = GrapheCLSCs[current][neighbor]        #On la change
        '''
    
def dijkstraPath(graphe, origin = 'A', destination = 'E'):
    # le tuple est (Precedent, temps)
    paths = {origin : (None, 0)}
    
    current_node = origin
    visited = set()

    while current_node != destination:
        visited.add(current_node)

        current_node_time = paths[current_node][1]

        #on parcourt tous les voisins du noeud courant
        for neighbour in graphe[current_node]:
            new_time = graphe[current_node][neighbour] + current_node_time

            if neighbour not in paths:
                paths[neighbour] = (current_node, new_time)
            else:
                current_shortest_time = paths[neighbour][1]
                if current_shortest_time > new_time:
                    paths[neighbour] = (current_node,new_time)
        
        next_destinations = {node : paths[node] for node in paths if node not in visited }

        current_node = min(next_destinations, key=lambda k:next_destinations[k][1])

        print(paths)


    path=[]
    while current_node is not None:
        path.append(current_node)
        next_node = paths[current_node][0]
        current_node = next_node

    path = path[::-1]
    return path
        

    


    


