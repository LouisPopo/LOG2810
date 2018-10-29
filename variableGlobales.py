
NI_MH = "NI-MH"
LI_ion = "LI_ion"

faible_risque = 'faible_risque'
moyen_risque = 'moyen_risque'
haut_risque = 'haut_risque'

niveau_risque = {
    1 : faible_risque,
    2 : moyen_risque,
    3 : haut_risque
}

vehicule = {
    1 : NI_MH,
    2 : LI_ion 
}

taux_decharge = {
    NI_MH : {
        faible_risque : (6/60),
        moyen_risque : (12/60),
        haut_risque : (48/60)
    },

    LI_ion : {
        faible_risque : (5/60),
        moyen_risque : (10/60),
        haut_risque : (30/60)
    }
}
