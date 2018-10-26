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

def plusCourtChemin(graphe, typeParcours = None, origine = '1', destination = '5'):
    print(graphe)
    
    visited, parcours = list(), list()
    unvisited = {node: float('inf') for node in graphe} #mets la distance a 'Infini' pour tous les points

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
        
        
    '''
        c

                                    #Ajoute le noeud trouve au CLSC visites
                                    #L'enleve des CLSCS non visites
        for neighbor in GrapheCLSCs[current]:                           #Cherche parmis les voisins de ce noeud
            if neighbor not in visited:                                             #Si on a pas deja visite le voisin
                if GrapheCLSCs[current][neighbor] < unvisited[neighbor]:        #Si la distance entre le noeud et son voisin est plus petite que celle qui avait avant  
                    unvisited[neighbor] = GrapheCLSCs[current][neighbor]        #On la change
        '''
    
        
    


    


