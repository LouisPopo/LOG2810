from enum import Enum

class Vehicule(Enum):
    NI_MH = 'NI-MH'
    LI_ion = 'LI-ion'

class Risque(Enum):
    faible = 'Faible Risque'
    moyen = 'Moyen Risque'
    haut = 'Haut Risque'

taux_decharge = {
    Vehicule.NI_MH : {
        Risque.faible : (6/60),
        Risque.moyen : (12/60),
        Risque.haut : (48/60)
    },

    Vehicule.LI_ion : {
        Risque.faible : (5/60),
        Risque.moyen : (10/60),
        Risque.haut : (30/60)
    }
}
