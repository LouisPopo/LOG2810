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

def plusCourtChemin(typeParcours = None, origine = '1', destination = '8'):
    visited, parcours = list(), list()
    unvisited = dict()

    for key in CLSCs:
        unvisited[key] = float('inf')                                   #mets la distance a 'Infini' pour tous les points

    unvisited[origine] = 0                                              #mets la distance a '0' pour le point de depart

    print("UNVISITED AU DEBUT")
    print(unvisited)

    for i in range(0,2) :
        closestNeighbor = min(unvisited, key= lambda x: unvisited.get(x))   #Trouve le noeud avec la plus petite distance parmis les unvisited. C'est 'origine' la 1ere fois
        print(str(i) + " EME FOIS ")
        print(closestNeighbor)
        visited.append(closestNeighbor)                                     #Ajoute le noeud trouve au CLSC visites
        del unvisited[closestNeighbor]                                      #L'enleve des CLSCS non visites
        for neighbor in GrapheCLSCs[closestNeighbor]:                           #Cherche parmis les voisins de ce noeud
            if neighbor not in visited:                                             #Si on a pas deja visite le voisin
                if GrapheCLSCs[closestNeighbor][neighbor] < unvisited[neighbor]:        #Si la distance entre le noeud et son voisin est plus petite que celle qui avait avant  
                    unvisited[neighbor] = GrapheCLSCs[closestNeighbor][neighbor]        #On la change
        print (unvisited)
        
    


    


