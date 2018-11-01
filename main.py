from graphesFunctions import *
from menu import menu
from dictionnaires import *

GrapheCLSCs = None

fakeDict = {
    'A' : {'B':3,'C':2},
    'B' : {'A':3,'C':6,'F':4},
    'C' : {'A':5, 'B':3,'F':8},
    'D' : {'F':12},
    'E' : {'B':4,'D':1}
}

def main():
    creerGraphe("centresLocaux.txt")
    
    a = testLongChemin('23',200)
    print(a)
main()