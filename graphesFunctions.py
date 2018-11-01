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
def creerGraphe(nomFichier):
    
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
    for noeud in GrapheCLSCs:
        print (str(noeud) + " : " + str(GrapheCLSCs[noeud]))

# Parametres : Risque.type, le noeud d'origine et la destinatinons (en string)
# Retourne un dictionnaire : (Chemin : [liste], TempsTotal : int, Batterie : int, Vehicule : Vehicule)
# OU None si impossible
def plusCourtChemin(risqueTransport, origine, destination, typeVehicule = Vehicule.NI_MH):

    chemin, tempsChemin = algoDijkstra(origine, destination)

    tauxDecharge = dictTauxDecharge[typeVehicule][risqueTransport]
    tempsDecharge80 = 80/tauxDecharge
    niveauBatterieFinal = BATTERIE_PLEINE - tauxDecharge*tempsChemin

    cheminTrouve = False
    resultat = None

    # Si la voiture se decharge avant d'arriver
    if(tempsChemin > tempsDecharge80):
        #On parcourt le chemin dans le sens inverse, et on trouve la premiere CLSC, ou on peut se recharger
        for clsc,tempsAPartirDOrigine in chemin[::-1]:
            if (tempsAPartirDOrigine < tempsDecharge80 and BorneRecharge[clsc]):
                print("On recharge a la borne : " + str(clsc))
                
                tempsBorneJusquaDestination = tempsChemin - tempsAPartirDOrigine
                batterieFinale = BATTERIE_PLEINE - tempsBorneJusquaDestination*tauxDecharge
                
                if(batterieFinale > 20):
                    tempsChemin += TEMPS_RECHARGE
                    cheminTrouve = True
                    break
    # Sinon, il est possible de faire le trajet sans recharger
    else:
        cheminTrouve = True
    
    resultat = {
        'Chemin' : creerListeChemin(chemin),
        'TempsTotal' : tempsChemin,
        'Batterie' : niveauBatterieFinal,
        'Vehicule' : typeVehicule
    }

    # Si la voiture se decharge en chemin, et qu'il n'y a pas de Bornes,
    # On calcule le plus court chemin de origine jusqua toutes les bornes de recharge ET
    # le plus cours chemin de toutes les bornes de recharge jusqu'a destination
    if(not cheminTrouve):
        print('Chemin le plus court ne contient pas de bornes de recharge')
        resultat = trouverPlusCourtCheminAvecBorneRecharge(tempsDecharge80, origine, destination, tauxDecharge)
        if resultat != None:
            resultat['Vehicule'] = typeVehicule
            cheminTrouve = True

    # Si on ne trouve toujours pas de chemin possible avec le vehicule NI-MH, on essaye avec
    # un vehicule LI-ion
    if(not cheminTrouve and typeVehicule == Vehicule.NI_MH):
        resultat = plusCourtChemin(risqueTransport,origine,destination,Vehicule.LI_ion)

    return resultat

# Retourne un tuple (set [noeud : temps a partir d'origine], temps total)
def algoDijkstra(origine, destination):
    # dict = {noeudCourant (noeudPrecedent, tempsAPartirOrigine)
    plusCourtsChemins = {origine : (None, 0)}
    
    noeudCourant = origine
    noeudVisites = set()

    while noeudCourant != destination:
        noeudVisites.add(noeudCourant)

        tempsOrigineJusquaNoeudCourant = plusCourtsChemins[noeudCourant][1]

        #on parcourt tous les voisins du noeud courant
        for voisin in GrapheCLSCs[noeudCourant]:
            tempsOrigineJusquaVoisin = GrapheCLSCs[noeudCourant][voisin] + tempsOrigineJusquaNoeudCourant

            if voisin not in plusCourtsChemins:
                plusCourtsChemins[voisin] = (noeudCourant, tempsOrigineJusquaVoisin)
            else:
                tempsActuel = plusCourtsChemins[voisin][1]
                if tempsOrigineJusquaVoisin < tempsActuel:
                    plusCourtsChemins[voisin] = (noeudCourant,tempsOrigineJusquaVoisin)
        
        prochainsNoeuds = {noeud : plusCourtsChemins[noeud] for noeud in plusCourtsChemins if noeud not in noeudVisites }

        noeudCourant = min(prochainsNoeuds, key=lambda k:prochainsNoeuds[k][1])

    chemin=[]
    # noeudCourant = destination
    # chemin = set tuples(noeud, time from origin)
    # On parcourt le dictionnaire 'plusCourtsChemins' : en partant de 'destination' et en allant ensuite au noeud present dans le tuple
    while noeudCourant is not None:
        chemin.append((noeudCourant, plusCourtsChemins[noeudCourant][1]))
        prochainNoeud = plusCourtsChemins[noeudCourant][0]
        noeudCourant = prochainNoeud

    #on inverse l'ordre du tableau
    chemin = chemin[::-1]
    return (chemin, plusCourtsChemins[destination][1])

# Retourne un dictionnaire (Chemin : [liste], TempsTotal : int, Batterie : int)
# OU None si impossible
def trouverPlusCourtCheminAvecBorneRecharge(tempsDecharge80, origine, destination, tauxDecharge):
    # On prend toutes les CLSCs qui ont des bornes de recharge
    idsCLSCsAvecBorne = set(filter(BorneRecharge.get, BorneRecharge))
     
    cheminsOrigineBornes = []

    for clsc in idsCLSCsAvecBorne:
        if clsc != origine:
            chemin = algoDijkstra(origine,clsc)
            if(chemin[1] < tempsDecharge80):
                cheminsOrigineBornes.append(chemin)

    resultat = None
    tempsMinimal = float('inf')

    for cheminJusquaBorne, tempsJusquaBorne in cheminsOrigineBornes:
        idBorne = cheminJusquaBorne[-1][0]              # On prend le dernier element de la liste, qui est un tuple 
                                                        # (noeud, temps a partir d'origine ), duquel on prend le noeud seulement
        cheminBorneJusquaDestination, tempsBorneJusquaDestination = algoDijkstra(idBorne,destination)
        
        if(tempsBorneJusquaDestination < tempsDecharge80) and (tempsJusquaBorne + tempsBorneJusquaDestination < tempsMinimal):
            tempsMinimal = tempsJusquaBorne + tempsBorneJusquaDestination
            resultat = {
                'Chemin' : creerListeChemin(cheminJusquaBorne) + creerListeChemin(cheminBorneJusquaDestination),
                'TempsTotal' : tempsJusquaBorne + tempsBorneJusquaDestination + TEMPS_RECHARGE,
                'Batterie' : BATTERIE_PLEINE - tempsBorneJusquaDestination*tauxDecharge
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
<<<<<<< HEAD
def extraireSousGraphe(categorie_transport, origine, typeVehicule):
    graphe = GrapheCLSCs
    noeudCourant = origine
    noeud_precedent = None
    tempsDecharge80 = 80/dictTauxDecharge[typeVehicule][categorie_transport]

    chemins_possibles = trouverCheminsPossibles(noeud_precedent, noeudCourant, tempsDecharge80, graphe, 0)

    plusLongChemin = max(chemins_possibles, key=lambda k:chemins_possibles[k][k][1])
    return [chemins_possibles[plusLongChemin][0], chemins_possibles[plusLongChemin][1]]
=======
def extraireSousGraphe(risque_transport, origine, type_vehicule):
    tauxDecharge = dictTauxDecharge[type_vehicule][risque_transport]
    temps_decharge_80 = 80/tauxDecharge
>>>>>>> f30c26b4686361a411848a3f593ab9fa9d361e1f

    plusLongChemin = testLongChemin(origine, temps_decharge_80, visited = set(), currentTime = 0, path = [])

<<<<<<< HEAD
def trouverCheminsPossibles(noeud_precedent, noeudCourant, tempsDecharge80, graphe, chemin_actuel):
    
    for voisin in graphe[noeudCourant][voisin]:
        chemins_possibles = {} #{0 : [[1,2,3,4], temps], 1: [[5,6,7], temps2]}
        voisins = []
        #Met tous les voisins dans voisins[] et enlever les noeuds deja visites
        
        for voisin in graphe[noeudCourant][voisin]:
            voisins.append(voisin)
        for voisin in voisins:
            if voisin in chemins_possibles[chemin_actuel][0]:
                voisins.remove(voisin)
        
        if voisins:
            for voisin in voisins:
                if (chemins_possibles[chemin_actuel][1] <= tempsDecharge80):
                    chemins_possibles[chemin_actuel][0].append(noeudCourant)
                    chemins_possibles[chemin_actuel][1] += graphe[noeud_precedent][noeudCourant]
                    noeud_precedent = noeudCourant
                    noeudCourant = voisin
        else:
            chemin_actuel += 1
    
    return chemins_possibles



    # graphe = GrapheCLSCs
    # plus_longs_chemins = {origine : (None, 0)}
    # noeudCourant = origine
    # noeudVisites = set()

    # tempsDecharge80 = 80/taux_decharge[typeVehicule][categorie_transport]

    # while(plus_longs_chemins[noeudCourant][1] < tempsDecharge80):
    #     noeudVisites.add(noeudCourant)

    #     temps_actuel = plus_longs_chemins[noeudCourant][1]

    #     #on parcourt tous les voisins du noeud courant
    #     for voisin in graphe[noeudCourant]:
    #         tempsOrigineJusquaVoisin = graphe[noeudCourant][voisin] + temps_actuel

    #         if voisin not in plus_longs_chemins:
    #             plus_longs_chemins[voisin] = (noeudCourant, tempsOrigineJusquaVoisin)
    #         else:
    #             temps_maximal_actuel = plus_longs_chemins[voisin][1]
    #             if tempsOrigineJusquaVoisin > temps_maximal_actuel:
    #                 if plus_longs_chemins[voisin][0] not in noeudVisites:
    #                     if plus_longs_chemins[voisin][0] != None:
    #                         plus_longs_chemins[voisin] = (noeudCourant, tempsOrigineJusquaVoisin)

    #     prochainsNoeuds = {noeud : plus_longs_chemins[noeud] for noeud in plus_longs_chemins if noeud not in noeudVisites }
    #     if(prochainsNoeuds):
    #         noeudCourant = max(prochainsNoeuds, key=lambda k:prochainsNoeuds[k][1])
    #     else:
    #         break

    # chemin = []

    # while noeudCourant is not None:
    #     chemin.append((noeudCourant, plus_longs_chemins[noeudCourant][1]))
    #     prochainNoeud = plus_longs_chemins[noeudCourant][0]
    #     noeudCourant = prochainNoeud

    # chemin = chemin[::-1]

    # return [chemin, temps_actuel]

def testLongChemin(origine, tempsAutonomie, noeudsVisites = [], tempsTotal = 0, chemin = []):

    if not noeudsVisites:
        noeudsVisites.append(origine)
    if not chemin:
        chemin.append(origine)
    
    cheminsPotentiels = []
=======
    return plusLongChemin[0]
    

def testLongChemin(origine, timeTo20, visited = set(), currentTime = 0, path = []):
    #print(origine, visited)
    cheminsTemp = []

    visited.add(origine)

    path.append(origine)
>>>>>>> f30c26b4686361a411848a3f593ab9fa9d361e1f

    voisins = list(GrapheCLSCs[origine].keys())
    voisinsToVisit = [node for node in voisins if node not in visited]

    
    if all(timeTo20 < GrapheCLSCs[origine][voisin] + currentTime for voisin in voisinsToVisit):
        return (path, currentTime)

    for voisin in [node for node in voisins if node not in visited]:
        if currentTime + GrapheCLSCs[origine][voisin] < timeTo20:
            
            copyCurrentTime = currentTime
            copyCurrentTime += GrapheCLSCs[origine][voisin]
            cheminsTemp.append(testLongChemin(voisin, timeTo20, visited, copyCurrentTime, path.copy()))

    return max(cheminsTemp, key=lambda item:item[1])
        
            