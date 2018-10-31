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
  

def extraireSousGraphe(categorie_transport, origine, type_vehicule=Vehicule.NINH):
    graphe = GrapheCLSCs
    noeud_courant = origine
    noeud_precedent = None
    temps_decharge_80 = 80/taux_decharge[type_vehicule][categorie_transport]

    chemins_possibles = trouverCheminsPossibles(noeud_precedent, noeud_courant, temps_decharge_80, graphe, 0)

    plusLongChemin = max(chemins_possibles, key=lambda k:chemins_possibles[k][k][1])
    return [chemins_possibles[plusLongChemin][0], chemins_possibles[plusLongChemin][1]]


def trouverCheminsPossibles(noeud_precedent, noeud_courant, temps_decharge_80, graphe, chemin_actuel):
    
    for voisin in graphe[noeud_courant][voisin]:
        chemins_possibles = {} #{0 : [[1,2,3,4], temps], 1: [[5,6,7], temps2]}
        voisins = []
        #Met tous les voisins dans voisins[] et enlever les noeuds deja visites
        
        for voisin in graphe[noeud_courant][voisin]:
            voisins.append(voisin)
        for voisin in voisins:
            if voisin in chemins_possibles[chemin_actuel][0]:
                voisins.remove(voisin)
        
        if voisins:
            for voisin in voisins:
                if (chemins_possibles[chemin_actuel][1] <= temps_decharge_80):
                    chemins_possibles[chemin_actuel][0].append(noeud_courant)
                    chemins_possibles[chemin_actuel][1] += graphe[noeud_precedent][noeud_courant]
                    noeud_precedent = noeud_courant
                    noeud_courant = voisin
        else:
            chemin_actuel += 1
    
    return chemins_possibles



    # graphe = GrapheCLSCs
    # plus_longs_chemins = {origine : (None, 0)}
    # noeud_courant = origine
    # noeuds_visites = set()

    # temps_decharge_80 = 80/taux_decharge[type_vehicule][categorie_transport]

    # while(plus_longs_chemins[noeud_courant][1] < temps_decharge_80):
    #     noeuds_visites.add(noeud_courant)

    #     temps_actuel = plus_longs_chemins[noeud_courant][1]

    #     #on parcourt tous les voisins du noeud courant
    #     for voisin in graphe[noeud_courant]:
    #         temps_origine_a_voisin = graphe[noeud_courant][voisin] + temps_actuel

    #         if voisin not in plus_longs_chemins:
    #             plus_longs_chemins[voisin] = (noeud_courant, temps_origine_a_voisin)
    #         else:
    #             temps_maximal_actuel = plus_longs_chemins[voisin][1]
    #             if temps_origine_a_voisin > temps_maximal_actuel:
    #                 if plus_longs_chemins[voisin][0] not in noeuds_visites:
    #                     if plus_longs_chemins[voisin][0] != None:
    #                         plus_longs_chemins[voisin] = (noeud_courant, temps_origine_a_voisin)

    #     prochains_noeuds = {noeud : plus_longs_chemins[noeud] for noeud in plus_longs_chemins if noeud not in noeuds_visites }
    #     if(prochains_noeuds):
    #         noeud_courant = max(prochains_noeuds, key=lambda k:prochains_noeuds[k][1])
    #     else:
    #         break

    # chemin = []

    # while noeud_courant is not None:
    #     chemin.append((noeud_courant, plus_longs_chemins[noeud_courant][1]))
    #     prochain_noeud = plus_longs_chemins[noeud_courant][0]
    #     noeud_courant = prochain_noeud

    # chemin = chemin[::-1]

    # return [chemin, temps_actuel]

    